| Call | Caller wanted (manual read) | Assistant logged | book_appointment ok | Tool-log problems |
|---|---|---|---|---|
| C-01 | book periodic | Appointment booked | yes | none |
| C-02 | status (JC-2274) | Appointment booked | no | FALSE_BOOKED; STATUS_TOOL_NOT_USED; TRANSFER_no_answer_NO_CALLBACK; SLOTS_CHECKED_NO_BOOKING |
| C-03 | price enquiry | Appointment booked | no | FALSE_BOOKED; UNGROUNDED_PRICE; SLOTS_CHECKED_NO_BOOKING |
| C-04 | status (JC-2291) | Transferred to advisor | no | STATUS_TOOL_NOT_USED |
| C-05 | price + book | Appointment booked | no | FALSE_BOOKED; UNGROUNDED_PRICE; SLOTS_CHECKED_NO_BOOKING |
| C-06 | rework complaint | Transferred to advisor | no | SLOTS_CHECKED_NO_BOOKING |
| C-07 | status (JC-2288) | No action | no | STATUS_TOOL_NOT_USED; SLOTS_CHECKED_NO_BOOKING |
| C-08 | book AC diagnostic | Appointment booked | yes | NO_start_local on slot S-4419; WRONG_TIME_TOLD; UNGROUNDED_PRICE |
| C-09 | book brake check | Appointment booked | yes | NO_start_local on slot S-4431; WRONG_TIME_TOLD |
| C-10 | pickup/drop enquiry | Appointment booked | no | FALSE_BOOKED; SLOTS_CHECKED_NO_BOOKING |
| C-11 | part status (JC-2296) | Callback requested | no | STATUS_TOOL_NOT_USED; CALLBACK_NO_DEADLINE; SLOTS_CHECKED_NO_BOOKING |
| C-12 | billing dispute | Transferred to advisor | no | SLOTS_CHECKED_NO_BOOKING |
| C-13 | book Sunday | Appointment booked | no | FALSE_BOOKED; BOOK_ERROR_IGNORED; INVENTED_SLOT_ID; SLOTS_CHECKED_NO_BOOKING |
| C-14 | status (JC-2302) | Callback requested | no | STATUS_TOOL_NOT_USED; SLOTS_CHECKED_NO_BOOKING |
| C-15 | insurance dent enquiry | No action | no | AVAIL_ERROR; SLOTS_CHECKED_NO_BOOKING |
| C-16 | status, 3rd call (JC-2287) | Transferred to advisor | no | STATUS_TOOL_NOT_USED; SLOTS_CHECKED_NO_BOOKING |
| C-17 | claim status (JC-2280) | No action | no | STATUS_TOOL_NOT_USED |
| C-18 | book 40k service | Appointment booked | yes | none |
| C-19 | wrong number | No action | no | none |
| C-20 | status, urgent (JC-2309) | Transferred to advisor | no | STATUS_TOOL_NOT_USED; SLOTS_CHECKED_NO_BOOKING |
