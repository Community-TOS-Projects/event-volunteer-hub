# Event Time Structure and Shift Requirements

## Problem
 Event creation currently records a date and a start time, but not an end time. The application also has no way to define volunteer shifts within an event. For long events, organizers may need multiple volunteer time blocks, and contributors need a shared definition of those blocks and their relationship to an event before designing the workflow or data model.

## Current System Behavior
- Event creation form includes start time only.
- No field exists for event end time.
- No model or workflow exists for shifts.
- Volunteers cannot be assigned to specific time blocks.
- Long events cannot be represented accurately.

## Expected Event Time Structure
An event should have a start time and an end time on its event date. The end time describes when the event is expected to finish. It is distinct from the start time and should be visible wherever organizers create or review an event.


The event's start and end establish the time window within which its shifts are expected to take place. Whether events may span midnight, and how that should be represented, remains an open question.

## Shift Definition
A shift is a named volunteer work period associated with one event. Long events may need multiple shifts so that volunteers can cover different parts of the event without each person being expected to volunteer for its entire duration.

### Required Shift Attributes


- **Name** — a short label that identifies the work period, such as “Setup” or “Afternoon check-in.”
- **Start time** — when volunteers assigned to the shift are expected to begin.
- **End time** — when the shift is expected to finish.
- **Capacity** — the maximum number of volunteers the shift can accommodate.
- **Event** — the event this shift belongs to.


The name, start time, end time, and capacity describe the shift, the event relationship associates it with its parent event. Whether additional attributes are needed, such as role or description, is undecided.

## Relationship Between Events and Shifts
- An event may contain one or more shifts.
- All shifts must fall within the event’s start and end time.
- Shifts may be sequential or overlapping (requires decision).
- Volunteers sign up for shifts, not the entire event.

## Expected Workflow in Event Creation
The event creation workflow should eventually allow:
- Entering event start and end time.
- Adding one or more shifts.
- Specifying shift attributes.
- Saving the event with its associated shifts.

## Potential Database Changes


The following changes are likely needed; they are design considerations, not an implemented schema:


- Add an event end-time field, likely named `end_time`, alongside the existing `time` field.
- Decide whether to keep and relabel `time` as the event start time or migrate/rename it to `start_time`. Preserve existing event start times when applying any schema migration.
- Create a `Shift` model with a foreign key to `Event`, plus fields for name, start time, end time, and capacity.
- Use a one-to-many relationship: an event can have multiple shifts, and each shift belongs to one event. A reverse relation from an event to its shifts would allow the application to display and manage them together.
- Add and apply database migrations for the event and shift schema changes.

## Open Questions


1. **Event dates and overnight events:** Can an event or shift cross midnight? If so, should shifts store full start/end datetimes or a date in addition to their times?
2. **Time boundaries:** Must an event end time be later than its start time, and must every shift fall entirely within the event's start/end window?
3. **Shift overlap:** May shifts for the same event overlap?
4. **Optional shifts:** Can an event be created without shifts, or must it have at least one?
5. **Capacity rules:** Must capacity be a positive number? Can it be unlimited, and what should happen when a shift reaches capacity?
6. **Volunteer assignment:** Should volunteers sign up for a specific shift, and should an event-level attendee remain distinct from a shift assignment?
7. **Additional shift details:** Do shifts need a role, description, location, or other fields beyond the required attributes listed above?
8. **Editing and deletion:** What should happen to existing volunteer assignments if an organizer edits or deletes a shift?
9. **Existing events:** Should existing events receive a blank/unknown end time, or should a default be selected during migration?

## Future Work
This documentation enables future issues such as:
- Adding end_time to the Event model.
- Creating the Shift model and migrations.
- Implementing shift creation in the UI.
- Adding volunteer shift sign‑up workflows.
- Writing tests for shift validation and scheduling.
