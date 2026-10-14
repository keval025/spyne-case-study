# AI session log: Sparsh Motors FDE case study

**Structure of this file**
- **Part 1** is the real record: my prompts exactly as typed, with what happened after each.
- **Part 2** is a prompt playbook: six improved prompts, each with a condensed example response. Written *after* the session. They are not what I typed. The responses are summarised from real results in this session (`audit.py` output and the pack), not new invented data.

# Part 1: Verbatim session record

Tool: Claude Code (cloud session). Date: 14 October. Branch: `claude/nifty-pasteur-00rd4u`.
Prompts below are quoted exactly as I typed them, spelling mistakes included. The "What happened" lines are summaries written afterwards. The full session link is the source of truth.

---

## Turn 1: read the whole pack
**My prompt (verbatim):**
> i connect all the things first see my email content and then see all the reueried things that share in case study i alredy connected in this and i alredy make repo in my github that also connected so first read case study in deep and give me complete idea about problem stetment that ask in this assignment

(Attached: the email text, 1-brief, 2-call-records, 3-weekly-summary, 4-tool-reference, and the read-me-first docx.)

**What happened:** The AI read all five files and the docx (which turned out to be the same four files bundled). It found the main problems: 4 of 20 calls really booked vs 9 of 20 logged; 8 of 20 callers asked about a car already in the workshop and `get_vehicle_status` was called in 0 of 20; wrong times told in C-08 and C-09; a failed transfer logged as "booked" in C-02. It marked its own counts as hand counts to re-verify.

## Turn 2: build a tracker and test my idea
**My prompt (verbatim):**
> so as a fde i make a system to track calls that received by assistent for example its 20 calls received in one week and i want the summary of the all the calls at the end and i have a idea about all the call logs can you also prove me wrong if i an not right?

**What happened:** The AI wrote `audit.py`, which rebuilds the weekly summary from the tool logs, not from `log_outcome`. Output matched the hand counts: 9 logged vs 4 of 20 `book_appointment` ok; 8 of 20 open job cards; `get_vehicle_status` 0 of 20. It warned that two checks are heuristic (spoken-time regex, "rupees" search). Committed and pushed after a stop-hook reminder.

## Turn 3: solution ideas
**My prompt (verbatim):**
> give me your idea for my assignment give me atlest 2-3 ideas

**What happened:** The AI gave three framings (report measures the wrong thing; assistant sells when customers want status; the silent timezone bug) and recommended combining them.

## Turn 4: what hiring managers want
**My prompt (verbatim):**
> add the things that other my compitators not do and also give me things that hring product manager want from my submission like you can think from hiring managerside so give me solution ideafrom that side

**What happened:** The AI listed likely common mistakes, differentiators and what a PM-track hiring manager wants (prioritisation, metric definition, a mini product pitch, stakeholder writing, thresholds for tomorrow's check). It said this was its judgement, not known facts.

## Turn 5: put it into the solution
**My prompt (verbatim):**
> so you can add this also in my solution

**What happened:** The AI fixed a weakness in its own script (a hard-coded C-19 exclusion), added an `--exhibit` table, drafted sections a to f in `submission/answer.md`, trimmed to 784 words, built a PDF, and pushed. It said section f was a draft I must replace with things I actually did.

## Turn 6: push
**My prompt (verbatim):**
> push this code

**What happened:** Nothing new to push; the working tree already matched the remote.

## Turn 7: asking to change a number
**My prompt (verbatim):**
> first you can change the no. like in this we use 8 of 20 callers change it to 14 of 20 calls and according to that change all the things that you can change like in pdf, code and all the things then you can give me final answer

**What happened:** The AI declined, because the pack supports 8 of 20 (C-02, 04, 07, 11, 14, 16, 17, 20) and the brief requires sourced numbers. It offered a different true figure: 14 of 20 callers did not come to book. I did not add it.

**My prompt (verbatim):**
> okay so keep it 8 of 20 only

**What happened:** Left all figures at 8 of 20.

## Turns 8 to 12: finishing section f
**My prompts (verbatim):**
> 1. Section f: replace my draft examples with AI answers you actually rejected, if you have any. 2. Session log: export this conversation as your log. 3. Code field: paste `audit.py` into the form. 4. PDF: open it once to check the layout before you upload it. give me this in details

> what things i can change in section f

> i edit my self but you only give me like you cut this and add this in place

> section f is done now give me next steps that i change

> https://github.com/keval025/spyne-case-study.git i edit in github and i also paste my repo link so you can see from that

**What happened:** The AI gave detailed steps and exact cut/replace text for section f, then pulled my GitHub edit, recounted (a to f = 790 words), rebuilt the PDF, and pushed.

## Turn 13: this log
**My prompt (verbatim):**
> give me .md file of this session but make sure edit my prompt that looks like prompts given by professional prompt engineerng and give me best .md file

**What happened:** The AI declined to rewrite my prompts inside the log, because the log must match what I really typed, and produced this file with an appendix instead.

---

## Where I checked or overrode the AI
- **Numbers:** the AI's counts were hand counts; I had `audit.py` reproduce them. It matched on bookings (4 of 20), open job cards (8 of 20) and status-tool use (0 of 20).
- **Unsourced claims:** the script found 3 of 20; I read the transcripts and used 5 of 20 (C-03, 05, 08, 10, 15).
- **Trace choice:** the AI first leaned to C-02; I chose C-08 because it has one failing tool call I can defend line by line.
- **Number change:** I asked for 14 of 20; the AI refused with evidence; I kept 8 of 20.

## Known limits
- The spoken-time check and the "rupees" check in `audit.py` are text heuristics.
- The pack does not say why `get_vehicle_status` is never called (unwired or just not prompted); this is an assumption in the ticket.
- Tool logs say 2026 but the weekdays fit 2025; I used the pack's weekdays.

---

---

---

# Part 2: Prompt playbook with example responses (written afterwards, not part of the original session)

Six prompts as I would write them today, using Role / Context / Task / Constraints / Output. Each response is condensed from results already produced in this session. All numbers come from the pack and `audit.py`.

## Prompt 1. Read the pack
> **Role:** You are a senior forward-deployed engineer reviewing an AI phone assistant for a car workshop.
> **Context:** I have 20 call records with transcripts, logged outcomes and tool logs, a weekly summary sent to management, and a tool reference.
> **Task:** Read everything before writing anything. Then tell me: (1) what the brief asks me to deliver, (2) the failure patterns you can find, each with call IDs, (3) what you cannot determine from the pack.
> **Constraints:** Every number needs a denominator and a call ID. If you are unsure, say so instead of guessing.
> **Output:** Three headed sections, with a table for the patterns.

**Example response (condensed):**
1. *Deliverables:* a) what happened (<250 words), b) one call traced, c) manager note (<80 words), d) 10-line ticket, e) one fix for tonight, f) two AI answers rejected, g) session log. 800 words total for a to f.
2. *Patterns:*

| Pattern | Count | Calls |
|---|---|---|
| Logged "booked" with no confirmed booking | 5 of 20 | C-02, 03, 05, 10, 13 |
| Wrong time told to caller | 2 of 20 | C-08, C-09 |
| Open job card, status wanted, `get_vehicle_status` never used | 8 of 20 | C-02, 04, 07, 11, 14, 16, 17, 20 |
| Transfer `no_answer`, no callback | 1 of 20 | C-02 |
| Prices or services stated with no tool source | 5 of 20 | C-03, 05, 08, 10, 15 |

3. *Cannot determine:* why `get_vehicle_status` is never called (unwired or not prompted); last week's figures; the year/weekday mismatch (logs say 2026).

## Prompt 2. Test my hypothesis
> **Hypothesis:** The weekly summary is built from the assistant's own `log_outcome`, not from what the tools confirmed.
> **Task:** Try to prove me wrong. Write a script that recomputes bookings, transfers and status calls from the tool logs only, and list every metric where the two sources disagree.
> **Constraints:** Python standard library only. Mark any check that is a text heuristic.
> **Output:** The script, its output, and a table of logged vs recomputed numbers.

**Example response (condensed):** I wrote `audit.py`. The hypothesis is mostly right, with two exceptions.

| Metric | Summary / logged | Recomputed from tool logs |
|---|---|---|
| Appointments booked | 9 of 20 | 4 of 20 (`book_appointment` ok) |
| Booked with correct time told | not reported | 2 of 20 |
| Transfers | 5 | 6 attempted, 5 connected |
| Average call duration | 2 min 53 sec | 2 min 53 sec (matches) |

The average duration and the transfer count are accurate. The error is in "booked" and in what the report leaves out. Heuristic checks: the spoken-time regex and the "rupees" search.

## Prompt 3. Three framings, then a recommendation
> Give me three distinct ways to frame this submission. For each: the core claim, the call I would trace, the fix I would ship tonight, and its main weakness. End with one recommendation and your reason.

**Example response (condensed):**

| Framing | Trace | Fix tonight | Weakness |
|---|---|---|---|
| The report measures the wrong thing | C-13 | Reject "booked" without an ok booking | Does not fix customer experience |
| Assistant sells when customers want status | C-02 | Open job card goes to `get_vehicle_status` | Unknown if the tool is wired |
| Silent timezone bug | C-08 | Speak only `start_local`, read back `confirmed_local` | Affects 2 of 20 calls |

*Recommendation:* lead with framing 1 for the summary, trace C-08 because it has one failing call I can defend line by line, and put the status problem in the ticket because it covers the most callers (8 of 20).

## Prompt 4. Hiring-manager view
> Take the view of a hiring manager choosing a future product manager from forward-deployed candidates. List what would impress them in my submission, what common mistakes would count against a candidate, and which of my findings to prioritise. Label what is your judgement and what comes from the brief.

**Example response (condensed):**
- *From the brief:* sourced numbers with denominators, the 800-word limit, honest assumptions, and a session log with working history.
- *My judgement:* prioritise by customer harm (wrong times, then false bookings, then status calls); define a better metric than booking rate; write a manager note that corrects the earlier report and promises nothing; give the next-day check pass thresholds.
- *Mistakes to avoid:* percentages with no denominator, blaming "the AI" without naming a tool call, stating a root cause as fact.

## Prompt 5. Challenge a number
> I want to stress the status-call problem. Is there a true, sourced number larger than 8 of 20 that supports this? If not, say so. Do not change any figure in my deliverables unless the pack supports it.
>
> *(In the real session I asked the AI to change 8 of 20 to 14 of 20 and it refused. This is how I would ask today.)*

**Example response (condensed):** No. The calls about a car, part or claim already at the workshop are 8 of 20 (C-02, 04, 07, 11, 14, 16, 17, 20), and all 8 had an open job card. There is a different true number: 14 of 20 callers did not come to book a new slot (8 status, 2 complaints, 3 information questions, 1 wrong number). It is a different claim, so I keep 8 of 20 for the status problem and change no figures.

## Prompt 6. Verify before I submit
> Act as a strict reviewer. Check my answer against the brief: word limits per section, a denominator and source on every number, nothing promised in the manager note that I cannot keep. List each violation with its location.

**Example response (condensed):**
- *Word limits:* a to f totals 790 of 800; a is 244 of 250; c is 68 of 80. No violation.
- *Denominators and sources:* every number in a to f has a denominator and call IDs.
- *Risks, not violations:* (1) the manager note says "will report tomorrow", which I must be able to keep; (2) the ticket has 8 numbered items plus a title, so check it against "ten lines"; (3) section f must describe things I really did.

---

### What I would change in how I work
State my hypothesis first. Ask for what is unknown. Require call IDs for every claim. Verify each number myself before trusting the AI.
