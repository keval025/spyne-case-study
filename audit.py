#!/usr/bin/env python3
"""Call tracker / auditor for the Sparsh Motors pack.

Usage: python3 -I audit.py path/to/2-call-records.md

Rebuilds the weekly summary from the TOOL LOGS (what actually happened) and
compares it with what the assistant claimed in log_outcome.
"""
import json
import re
import sys
from datetime import datetime, timedelta

IST = timedelta(hours=5, minutes=30)


def parse(text):
    calls = []
    for blk in re.split(r"\n### (?=C-\d+)", text)[1:]:
        head = blk.splitlines()[0]
        m = re.match(r"(C-\d+) \| (\w+), ([\d:]+ [ap]m) \| (\d+) min (\d+) sec", head)
        cid, day, clock, mi, se = m.groups()
        logged = re.search(r"Logged outcome: (.+)", blk).group(1).strip()
        assistant = re.findall(r"> \*\*Assistant:\*\* (.+)", blk)
        caller = re.findall(r"> \*\*Caller:\*\* (.+)", blk)
        code = re.search(r"```\n(.*?)```", blk, re.S).group(1)
        events = []
        for line in code.splitlines():
            t = re.match(r"(\d\d:\d\d:\d\d)\s+(\w+)\s+(\{.*\})\s*$", line)
            if t:
                events.append({"ts": t.group(1), "tool": t.group(2),
                               "args": json.loads(t.group(3)), "raw": ""})
            elif line.strip() and events:
                events[-1]["raw"] += line.strip().lstrip("-> ").strip()
        for e in events:
            e["ret"] = json.loads(e["raw"])
        calls.append({"id": cid, "day": day, "clock": clock,
                      "secs": int(mi) * 60 + int(se), "logged": logged,
                      "assistant": assistant, "caller": caller, "ev": events})
    return calls


def tools(c, name):
    return [e for e in c["ev"] if e["tool"] == name]


def spoken_times(c):
    out = []
    for line in c["assistant"]:
        for h, mm, ap in re.findall(r"(\d{1,2})(?::(\d\d))? ?(am|pm)", line):
            h = int(h) % 12 + (12 if ap == "pm" else 0)
            out.append((h, int(mm or 0), line))
    return out


def audit(c):
    f = []  # findings
    lk = tools(c, "lookup_customer")[0]["ret"]
    jobs = lk.get("open_job_cards") or []
    oks = [e for e in tools(c, "book_appointment") if e["ret"].get("status") == "ok"]
    c["real_booking"] = bool(oks)
    c["open_jobs"] = bool(jobs)

    if c["logged"] == "Appointment booked" and not oks:
        f.append("FALSE_BOOKED: logged booked, no book_appointment ok")
    for e in tools(c, "book_appointment"):
        if "error" in e["ret"]:
            f.append(f"BOOK_ERROR_IGNORED: {e['ret']['error']} (slot {e['args']['slot_id']})")
        offered = {s["slot_id"] for a in tools(c, "check_availability")
                   for s in a["ret"].get("slots", [])}
        if e["args"]["slot_id"] not in offered:
            f.append(f"INVENTED_SLOT_ID: {e['args']['slot_id']} never returned by check_availability")
    if jobs and not tools(c, "get_vehicle_status"):
        f.append(f"STATUS_TOOL_NOT_USED: open job card {jobs}, get_vehicle_status never called")
    for e in tools(c, "transfer_to_advisor"):
        if e["ret"].get("status") != "connected" and not tools(c, "log_callback"):
            f.append(f"TRANSFER_{e['ret'].get('status')}_NO_CALLBACK")
    for e in tools(c, "log_callback"):
        if e["args"].get("deadline_local") is None:
            f.append("CALLBACK_NO_DEADLINE")
    for e in tools(c, "check_availability"):
        if "error" in e["ret"]:
            f.append(f"AVAIL_ERROR: {e['ret']['error']} {e['args']['service_type']}")
    # time told vs time booked
    for b in oks:
        conf = datetime.strptime(b["ret"]["confirmed_local"][:16], "%Y-%m-%d %H:%M")
        slot = next(s for a in tools(c, "check_availability")
                    for s in a["ret"]["slots"] if s["slot_id"] == b["args"]["slot_id"])
        if "start_local" not in slot:
            f.append(f"NO_start_local on slot {slot['slot_id']} ({b['args']['service_type']})")
        told = [(h, m) for h, m, _ in spoken_times(c)]
        if (conf.hour, conf.minute) not in told:
            f.append(f"WRONG_TIME_TOLD: booked {conf:%H:%M} IST, assistant said "
                     f"{sorted(set('%02d:%02d' % t for t in told))}")
    if any("rupees" in l for l in c["assistant"]):
        f.append("UNGROUNDED_PRICE: price quoted, no tool returns prices")
    n_av = len(tools(c, "check_availability"))
    if n_av and not oks:
        f.append(f"SLOTS_CHECKED_NO_BOOKING (x{n_av})")
    return f


def main(path):
    calls = parse(open(path, encoding="utf8").read())
    n = len(calls)
    allf = {}
    for c in calls:
        allf[c["id"]] = audit(c)

    print(f"{'ID':5} {'logged outcome':22} real_book open_job  findings")
    for c in calls:
        fl = allf[c["id"]]
        print(f"{c['id']:5} {c['logged']:22} {str(c['real_booking']):9} {str(c['open_jobs']):8} "
              f"{len(fl)}")
        for x in fl:
            print(f"        - {x}")

    def cnt(pred):
        ids = [c["id"] for c in calls if pred(c)]
        return f"{len(ids)} of {n}  {ids}"

    has = lambda c, key: any(x.startswith(key) for x in allf[c["id"]])
    print("\n=== SUMMARY (from tool logs) ===")
    print("Logged 'booked'          :", cnt(lambda c: c["logged"] == "Appointment booked"))
    print("book_appointment ok      :", cnt(lambda c: c["real_booking"]))
    print("booked but false         :", cnt(lambda c: has(c, "FALSE_BOOKED")))
    print("booked, wrong time told  :", cnt(lambda c: has(c, "WRONG_TIME")))
    print("booked correctly         :", cnt(lambda c: c["real_booking"] and not has(c, "WRONG_TIME")))
    print("open job card on lookup  :", cnt(lambda c: c["open_jobs"]))
    print("get_vehicle_status used  :", cnt(lambda c: bool(tools(c, "get_vehicle_status"))))
    print("check_availability used  :", cnt(lambda c: bool(tools(c, "check_availability"))))
    print("transfers attempted      :", cnt(lambda c: bool(tools(c, "transfer_to_advisor"))))
    print("transfers connected      :", cnt(lambda c: any(e["ret"].get("status") == "connected"
                                                          for e in tools(c, "transfer_to_advisor"))))
    print("transfer no_answer       :", cnt(lambda c: has(c, "TRANSFER_")))
    print("price quoted (ungrounded):", cnt(lambda c: has(c, "UNGROUNDED_PRICE")))
    print("leads left, no callback  :", cnt(lambda c: has(c, "SLOTS_CHECKED_NO_BOOKING")
                                              and not tools(c, "log_callback")
                                              and not tools(c, "transfer_to_advisor")
                                              and not c["open_jobs"] and c["id"] != "C-19"))
    avg = sum(c["secs"] for c in calls) / n
    print(f"avg duration             : {int(avg // 60)} min {round(avg % 60)} sec over {n} calls")


if __name__ == "__main__":
    main(sys.argv[1])
