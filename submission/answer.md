# FDE case study: Sparsh Motors, Kothrud (KTD-04), 18 to 23 August

## a. What happened this week

The summary says 9 of 20 calls ended in a booking. The tool logs show `book_appointment` returned `ok` in 4 of 20 (C-01, 08, 09, 18). The other 5 "booked" calls (C-02, 03, 05, 10, 13) never reached a confirmed booking. In C-13 the assistant sent an invented slot ID and got `WORKSHOP_CLOSED`.

Of the 4 real bookings, 2 gave the caller the wrong time. C-08: told 10:00, booked 15:30 IST. C-09: told 9:30, booked 15:00 IST. Diagnostic and inspection slots came back without `start_local`. Correct end to end: 2 of 20 (C-01, C-18).

8 of 20 callers asked about a car or claim already at the workshop (C-02, 04, 07, 11, 14, 16, 17, 20). All 8 had an open job card on lookup. `get_vehicle_status` was called in 0 of 20 calls. None of the 8 got a status; 3 reached an advisor. In C-02 the transfer got `no_answer`, no callback was logged, and the caller was told someone would get in touch.

Slots were checked in 17 of 20 calls. 5 of 20 callers left with no booking and no callback (C-03, 05, 10, 13, 15). 5 of 20 calls stated prices or services no tool supplies (C-03, 05, 08, 10, 15).

No source in the pack: last week's figures (17 calls, 6 booked). "100% answer rate" only counts calls the assistant received.

Assumption: the pack's weekdays are right (Mon 18 Aug); the logs say 2026.

## b. Trace: C-08, Tue 4:50 pm

- 16:50:21 `lookup_customer` returns C6455, no open jobs. Fine.
- **16:52:05 `check_availability` (diagnostic) is where it goes wrong.** It returns S-4419 with `start` 10:00Z and no `start_local`. The assistant read the UTC clock as local and told the caller "Wednesday 10 am". 10:00Z is 15:30 IST.
- 16:53:11 `book_appointment` returns `ok`, `confirmed_local` 15:30 IST. The assistant did not compare this with what it had said, and passed `vehicle: "unknown"` without asking.
- 16:53:30 `log_outcome` booked, notes "told customer 10 am". The log records the wrong time.

Why: the reference says to speak `start_local`. When it is missing the assistant fell back to `start`. The caller arrives 5 h 30 min early.

## c. Note to the workshop manager

The report overstated bookings. Of 20 calls, 4 were truly confirmed, not 9, and 2 of those 4 callers were given the wrong time. Please phone the customers on appointments A-9058 and A-9061 to confirm their times. Also, 8 of 20 callers were asking about cars already with you and got no update. I am fixing this and will report tomorrow.

## d. Ticket for engineering

**Assistant logs false bookings, speaks UTC times, never calls get_vehicle_status (site KTD-04)**

1. Evidence: 20 calls, 18 to 23 Aug. Repro: `python3 -I audit.py 2-call-records.md`.
2. Bug 1: `check_availability` for diagnostic and inspection omits `start_local` (S-4419, S-4431). Assistant spoke the UTC hour: C-08 said 10:00, booked 15:30 IST; C-09 said 9:30, booked 15:00. Fix: always return `start_local`; assistant reads back `confirmed_local`.
3. Bug 2: `log_outcome: booked` accepted with no prior `book_appointment` ok, in 5 of 20 calls (C-02, 03, 05, 10, 13). C-13 sent slot_id `S-SUN-0900`, never returned by any tool. Fix: reject server side.
4. Bug 3: `get_vehicle_status` called 0 of 20; 8 of 20 had open job cards and wanted status. First check whether the tool is registered for the assistant; then route non-empty `open_job_cards` to it.
5. `transfer_to_advisor` `no_answer` (C-02) needs `log_callback`; callbacks need `deadline_local` (C-11 is null).
6. Assistant states prices, pickup and insurance no tool supplies (C-03, 05, 08, 10, 15). It should hand off instead.
7. Confirm `bodyshop` off at KTD-04 is intended (C-15). Build the weekly report from tool results, not `log_outcome`.
8. Accept: on the next 20 calls, 0 false bookings, every spoken time equals `confirmed_local`, every open-job status call uses `get_vehicle_status`.

## e. Fix I would make tonight

Prompt change with four rules: speak only `start_local` and read back `confirmed_local` after booking; log "booked" only after `book_appointment` returns `ok`; if `open_job_cards` is non-empty call `get_vehicle_status`, and if that fails offer a callback with a deadline, never a slot; after `no_answer` always `log_callback`.

Tomorrow I run `audit.py` on the day's calls. Pass: 0 FALSE_BOOKED, 0 WRONG_TIME_TOLD, 0 STATUS_TOOL_NOT_USED. Guardrail: transfers should not rise because of the new rules.

## f. Two AI answers I did not take

1. Unsourced claims. The AI's script found 3 of 20 calls, by searching for "rupees". I read every transcript and found 5 of 20, adding C-10 (pickup charge) and C-15 (insurance). I used 5.
2. Which call to trace. The AI first leaned to C-02, which has four problems at once. I chose C-08 because it has one failing tool call (`check_availability`, 16:52:05) that I can defend line by line.
