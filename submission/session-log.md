# AI session log: Sparsh Motors FDE case study

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

# Appendix (written afterwards, not part of the original session)

This shows how I would phrase my main prompts today. It is a reflection on my prompting, not a record of what I typed.

**Turn 1, better version:**
> Role: you are helping me prepare an FDE case study. Task: read the brief and the 20 call records. Before writing anything, tell me (1) what the brief asks for, (2) the failure patterns you can find, each with call IDs, and (3) what you cannot determine from the pack. Constraint: every number needs a denominator and a source.

**Turn 2, better version:**
> My hypothesis is that the weekly summary is built from the assistant's own log_outcome, not from tool results. Try to prove me wrong. Write a script that recomputes the key metrics from the tool logs, and list any number where the two disagree.

**Turn 7, better version:**
> I want to emphasise the status-call problem. Is there a true, sourced number larger than 8 of 20 that supports this? If not, say so.

**What I would change in how I work:** state my hypothesis first, ask for what is unknown, and require call IDs for every claim.
