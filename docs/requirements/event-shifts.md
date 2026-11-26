# Event Time Structure and Shift Requirements

## Problem
Event creation currently stores a date and a start time, but does not define an event end time or a way to represent multiple volunteer work periods within a single event. For longer events, organizers may need to assign volunteers to different time periods. The application needs a clear definition of how event times, shifts, volunteer assignments, and attendance records relate before this workflow is extended.

## Current System Behavior
- Event creation includes a date and a start time.
- Event end time is not represented.
- There is no defined shift workflow for assigning volunteers to specific work periods.
- Event-level attendance/RSVP is distinct from assigning a volunteer to a particular shift.
- Attendance status and hours are not yet defined as a complete workflow, either for an event or for a specific shift.
- Long events cannot be represented clearly when work is distributed over time.

## Key Definitions
The requirements below distinguish between related concepts that should not be conflated:

- **Event**: the overall volunteer opportunity, with an event date and a start/end time on that date.
- **Shift**: a time period within an event during which volunteers are expected to work. A shift describes when coverage is needed; it does not, by itself, specify the role or work to perform.
- **Position**: a role or job type needed during a shift (for example, check-in volunteer, setup lead, cleanup crew). A position describes what kind of help is needed, not when the work occurs.
- **Task**: a specific activity to be performed during a shift. A task describes work to do, not a time period or role.
- **Assignment**: the scheduling of a volunteer to a shift, optionally identifying their position and tasks. The assignment is distinct from the shift, position, and tasks.
- **Event attendee**: a person who has indicated an intent to attend an event, independent of a particular volunteer assignment.
- **Attendance record**: a record of a person's attendance status and hours for an event, optionally associated with a shift. This is distinct from RSVP and assignment.
- **Event capacity**: the required finite, positive maximum number of distinct people participating in an event, whether attending as an RSVP attendee, as a volunteer, or both. A person counts once toward this limit even if they RSVP and volunteer.
- **Shift capacity**: the required finite, positive maximum number of distinct volunteers assigned to a particular shift. A volunteer counts once toward a shift's limit, regardless of how many positions or tasks they perform within it.

## Event Time Structure
An event must have a defined start and end time, and both must fall on the event date. Events that continue past midnight or span multiple dates are not supported by this time model.

The end time must be later than the start time. Shifts follow the same-date rule and must be fully contained within the event's time window.

## Shift Definition
A shift is a named volunteer work period associated with a single event. Shifts allow an event to be divided into multiple work blocks so that volunteers can cover different portions of the event without each person being expected to serve for the entire event.

### Required Shift Information
The following describes the information needed to define a shift, not a prescribed data model or implementation:

- **Name** — a short label identifying the work period, such as “Setup” or “Afternoon check-in.”
- **Event** — the event in which the shift takes place.
- **Start and end** — times on the event date when the shift is expected to begin and end. The end must be later than the start, and the shift must fit within the event time window.
- **Capacity** — the required finite, positive maximum number of volunteers who may be assigned to this shift.
- **Description** — optional explanatory text; it is not required.

An event may have no shifts. When shifts are defined, they must not overlap one another.

## Relationship Between Events and Shifts
- An event may contain zero or more shifts.
- Each shift is associated with exactly one event.
- Event and shift start/end times fall on the event date. Current project expectations do not support cross-midnight and multi-date events and shifts. This can be revisited in the future if required so.
- Each shift must be fully contained within the event's time window, and shifts for the same event must not overlap.
- Event-level attendees and shift-level volunteer assignments serve different purposes and should remain distinct.
- A person may RSVP, volunteer for one or more shifts, or do both. A volunteer assignment does not automatically create an RSVP. The event capacity counts each distinct person once, regardless of whether they RSVP and/or volunteer.
- An attendance record relates to an event and may optionally refer to a shift. If it refers to a shift, that shift must belong to the same event.
- Event capacity limits the total number of distinct event participants. Shift capacity limits the number of volunteers assigned to that shift. Both are finite, positive, required limits; an unlimited-capacity option is not supported. The sum of shift capacities may exceed event capacity, but the event capacity is an overall limit: no RSVP or volunteer assignment may cause the number of distinct event participants to exceed it.
- A participant may not be added as an RSVP attendee or assigned to a shift if doing so would exceed the event capacity. A volunteer may not be assigned to a shift if doing so would exceed that shift's capacity.

## Expected Workflow
The workflow should support the following activities:
- Define the event's date and overall time window.
- Set a finite event capacity for the maximum number of distinct participants.
- Optionally define shifts. Each shift has a time window contained within the event, does not overlap another shift, and has a finite volunteer capacity.
- Describe the roles needed using positions and the work to be done using tasks; neither changes the shift's time window or capacity.
- Assign volunteers to shifts, optionally identifying their positions and tasks. Enforce both the event capacity and the shift capacity when making assignments.
- Record event attendance status and hours, optionally associated with one of that event's shifts.

The event may be created without shifts. An RSVP attendee and a volunteer assignment are distinct, and a volunteer assignment does not automatically create an RSVP; the same person counts only once toward event capacity. Shifts do not overlap. Both event and shift capacities are required finite positive limits, and event capacity remains the overall limit even when the sum of shift capacities is greater.

## Potential Database Considerations
These are areas the eventual design must account for, not prescribed implementation details:

- Represent the event's date and same-date start/end times; reject an end time that is not later than its start.
- Represent each shift's association with one event and its same-date time period; require it to be within the event window and non-overlapping with other shifts for that event.
- Represent event capacity separately from each shift's capacity. Both limits are finite, required, and enforced against distinct participants and assigned volunteers respectively.
- Keep event RSVP, volunteer assignments, and attendance status/hours conceptually distinct, even if the eventual design relates them.
- Define what happens to related assignments and attendance information when an event, shift, or volunteer account is removed.

## Open Questions
1. **Assignment scope:** Can a volunteer hold more than one position or task during a shift, and how should those duties be communicated?
2. **Editing and deletion:** What happens to existing volunteer assignments if a shift is edited or deleted?
3. **Existing data migration:** How should existing events be handled when the event model is updated to include an end time or shift support?
4. **Multi-date Event Shifts** How should multi-date events be dealt with if events are required to cross midnight in the future as current project works with event shifts on the event date? 

## Future Work
This documentation supports future implementation work such as:
- Implementing the same-date event and shift time rules, including containment and non-overlap validation.
- Designing the eventual representation of shifts, volunteer assignments, and enforcement of the defined event and shift capacity rules.
- Defining the attendance record model for event attendance status and hours, with an optional association to a shift belonging to that event.
- Implementing the rule that shift assignment does not automatically create an event RSVP and completing the attendance-record workflow.
- Implementing the user workflow for adding and editing shifts, assigning volunteers, and recording attendance.
- Writing tests for event and shift validation, assignment behavior, attendance, and deletion rules.
- Defining how existing assignments are handled when shifts are edited or deleted and how existing events are migrated.