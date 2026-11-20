# Pull Request Reference

# Event Time Structure and Shift Requirements - PR 27

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


end PR 27
_______________________________________________________________________________________________

# Volunteer Sign-Up Requirements - PR 39

Related issue: #36. Builds on the shift definitions in [`event-shifts.md`](event-shifts.md) (issue #26).
"§" numbers refer to sections of [Unified Proposal v2.0](../EventVolunteerManagement_Proposal_v2.0.pdf).

## Why this document exists
The proposal says the system supports "both direct registration and registration that requires coordinator approval" and that coordinators "define volunteer positions and capacities" (§3). It does not say what a volunteer signs up for, when approval is needed, or what happens when a shift is full. This document answers those questions so everyone builds sign-up the same way.

## What the app does today
- A signed-in user clicks "Attend" on an event and is signed up right away.
- There is no approval step and no limit on how many people can sign up.
- Users sign up for a whole event. There are no shifts, positions, or tasks yet.
- "Cancel Attendance" deletes the sign-up completely.
- There are no volunteer or coordinator roles. Any signed-in user can do everything.

## Key terms
Shift, position, task, assignment, RSVP, attendance record, event capacity, and shift capacity are defined in `event-shifts.md`. This document uses those definitions and adds one term.

| Term | Meaning | How it relates to `event-shifts.md` |
|------|---------|-------------------------------------|
| **Sign-up** | A volunteer's request to work a shift. It has a status (see R6). | A confirmed sign-up becomes an **assignment**. A sign-up is not an RSVP and not an attendance record. |

## Requirements

| # | Requirement | Proposal source | Open question |
|---|-------------|-----------------|---------------|
| R1 | Volunteers sign up for a **shift**. A volunteer may sign up for more than one shift in the same event. | §1, §3 | Q7 (events with no shifts) |
| R2 | A volunteer cannot have two active sign-ups for the same shift. A volunteer may sign up again after cancelling. | §4 Database | |
| R3 | **Direct sign-up:** the volunteer is confirmed right away if there is room. | §3 | |
| R4 | **Approval sign-up:** the sign-up is "pending" until a coordinator approves or declines it. | §3 | Q2 (who decides), Q3 (do pending sign-ups hold a spot) |
| R5 | A coordinator, not the volunteer, picks which type of sign-up an event uses. | §3, §4 Back End | Q2 |
| R6 | Each sign-up has a status: pending, confirmed, declined, or cancelled. This is separate from the attendance status in an attendance record. | §3, §4 Database | Q4 (waitlisted status) |
| R7 | **When a shift or the event is full,** new sign-ups are blocked and the volunteer sees which one is full. A sign-up is blocked if it would go over the shift capacity or the event capacity. | §1, §4 Database | Q4 (waitlist) |
| R8 | Both capacity limits are enforced by the server, so two people cannot take the last spot. A person who is already an RSVP attendee or already has another shift in the event is not counted twice toward event capacity. | §4 Database | |
| R9 | A volunteer can cancel their own sign-up. Cancelling frees the spot. | §1, §3 | Q5 (cutoff time) |
| R10 | A cancelled sign-up is kept with status "cancelled," not deleted, so the sign-up history stays accurate. | §3 | |
| R11 | Volunteers get an email when they are confirmed, approved, or declined. | §3, §4 Communication | |
| R12 | Volunteers under 18 may need a chaperone confirmation before they are confirmed. | §3, §7 Assumptions | Q6 |
| R13 | Signing up for a shift does not create an RSVP, and RSVPing does not sign a person up for a shift. | §3 | |
| R14 | Volunteers do not choose positions or tasks when they sign up. A coordinator may add them to the assignment later. | §3 | Q1 (positions) |

## Open questions
- **Q1.** Can volunteers ask for a position when they sign up, or does a coordinator always choose it?
- **Q2.** Who counts as a coordinator, and is approval set per event or per shift?
- **Q3.** Does a pending sign-up hold a spot while it waits for approval?
- **Q4.** When a shift is full, do we only block sign-ups, or also offer a waitlist?
- **Q5.** Can volunteers cancel at any time, or is there a cutoff (for example, 24 hours before)?
- **Q6.** Does the under-18 chaperone check happen before, after, or instead of coordinator approval?
- **Q7.** An event may have no shifts (`event-shifts.md`). Can volunteers sign up for an event with no shifts, or is RSVP the only option?

end PR 39
_________________________________________________________________________________________________

# BUILDDAY NOTES/ISSUE FOUND: 

Candidate Issue Title: 

Align Volunteer Participation Models with PR27 and PR39 Requirements 

Evidence the Problem Exists:  

PR27 and PR39 define RSVP, Sign-Up, Assignment, and Attendance as separate concepts with distinct responsibilities and workflows. The current PR29 implementation contains Event.attendees, Shift.volunteers, and Attendance, but these relationships do not fully reflect the distinctions described in the approved requirements documentation. 

PR27 establishes separate definitions for: 

Event attendee (RSVP) 

Assignment 

Attendance record 

PR39 further defines: 

Sign-Up 

Assignment workflow 

Approval workflow 

The current PR29 implementation contains: 

Event.attendees 

Shift.volunteers 

Attendance 

Without clearly separating the documented workflows. 

Why It Matters:  

Resolving this issue establishes clear boundaries between RSVP, Sign-Up, Assignment, and Attendance workflows. This improves data integrity, reduces ambiguity for future contributors, and provides a stable foundation for capacity enforcement, approval workflows, attendance tracking, and volunteer scheduling features. 

 

Scope / Out of Scope:  

In Scope  

Analyze the current relationship overlap between:  

Event.attendees 

Shift.volunteers 

Attendance 

Define distinct database responsibilities for:  

RSVP 

Sign-Up 

Assignment 

Attendance 

Revise the database design so Attendance represents attendance information only. 

Replace or redesign implicit participation relationships that currently use Shift.volunteers to represent sign-up or assignment behavior. 

Define the lifecycle relationship between RSVP, Sign-Up, Assignment, and Attendance records. 

Identify required schema changes and migration impacts. 

Define verification requirements and required automated tests. 

Out of Scope:  

Organization-to-Account relationship design. 

Organization-to-Event relationship design. 

Shift overlap validation implementation. 

Additional event time validation rules beyond existing requirements. 

Attendance/Event/Shift consistency enforcement implementation. 

Existing event end-time migration strategy. 

Coordinator role implementation. 

Email notification workflows. 

Waitlist functionality. 

Volunteer position and task assignment workflows. 

Frontend sign-up, RSVP, or attendance user interfaces. 

Problem:  

PR29 introduced Attendance, Shift, and related volunteer relationships; however, subsequent requirements work in PR27 and PR39 clarified that RSVP, Sign-Up, Assignment, and Attendance represent distinct concepts with different workflows and lifecycle states. 

The current relational model contains overlapping responsibilities: 

Attendance currently contains sign-up and approval workflow statuses. 

Shift.volunteers functions as an implicit assignment/sign-up structure. 

RSVP, Sign-Up, Assignment, and Attendance relationships are not represented as distinct concepts despite being defined separately in project documentation. 

As a result, the current implementation does not fully align with approved project requirements and may cause ambiguity in future volunteer-management workflows. 

Connection to Partnership Responsibility:  

This issue establishes the foundational data architecture and domain boundaries for the Event Volunteer Hub. It impacts all downstream modules, including coordinator dashboards, user registration portals, and hour-verification workflows, ensuring data integrity and clean separation of concerns across event participation states. 

Work to Complete:  

Review the participation concepts defined in PR27 and PR39 and compare them against the current PR29 implementation. 

Analyze overlaps and ambiguities between:  

Event.attendees 

Shift.volunteers 

Attendance 

Design and implement a relational structure that represents RSVP, Sign-Up, Assignment, and Attendance as distinct concepts with clearly defined responsibilities. 

Refactor existing relationships as necessary to remove overlapping responsibilities and implicit workflow behavior. 

Implement any required database models and relationships needed to support RSVP, Sign-Up, Assignment, and Attendance independently. 

Replace or redesign the current Shift.volunteers many-to-many relationship if it cannot adequately represent the sign-up and assignment requirements documented in PR39. 

Ensure Attendance records store attendance-specific information only and are no longer responsible for sign-up or approval workflows. 

Update migrations, model tests, and relationship documentation to reflect the revised design. 

Document deferred architectural concerns and future follow-up work identified during implementation. 

Acceptance Criteria:  

Observable completion conditions that can later guide verification. 

RSVP participation is represented separately from volunteer sign-ups. 

Volunteer sign-up records support the workflow states defined in PR39, including pending, approved, declined, cancelled, and any other approved project states. 

Volunteer assignments are represented separately from RSVP and attendance concepts. 

Attendance records contain attendance-specific information only and do not manage sign-up approval workflows. 

The current implicit use of Shift.volunteers as a sign-up or assignment mechanism is replaced or revised to align with PR27 and PR39 requirements. 

Relationships between RSVP, Sign-Up, Assignment, and Attendance are documented and distinguishable within the schema. 

Required database migrations are created and apply successfully. 

Automated tests validate the revised relationships and workflow behavior. 

Existing event and shift functionality continues to pass regression testing. 

Deferred concerns identified by the maintainer (organization relationships, overlap validation, event-time validation, attendance consistency rules, and migration follow-up work) are documented for future implementation. 

Dependencies / Questions:  

Questions:  

Should pending sign-ups consume shift capacity? 

Should assignment remain distinct from sign-up records after approval? 

How should existing attendance records be migrated if status fields are removed? 

What relationship should exist between RSVP participation and sign-up participation for event-capacity calculations? 

Dependencies: 

Database and Migration Order: Any redesign of RSVP, Sign-Up, Assignment, and Attendance relationships will require modification or replacement of existing foreign keys and implicit relationships currently associated with Shift.volunteers. 

API and Controller Refactoring: Existing endpoints and business logic may require updates so the system can distinguish between RSVP participation, volunteer sign-up requests, volunteer assignments, and attendance records. 

Test Updates: Existing model, view, and workflow tests will require revision to reflect the new relationship structure and prevent regressions. 

Engineering Rationale:  

This issue is appropriately scoped because it focuses on a single architectural problem: the mismatch between the participation concepts defined in PR27 and PR39 and the relationships currently implemented in PR29. The issue is limited to the data model and relationship design. It does not attempt to implement volunteer interfaces, coordinator workflows, notifications, organization ownership, or other future features. By focusing on RSVP, Sign-Up, Assignment, and Attendance as separate concepts, the work establishes a clearer and more maintainable foundation for future volunteer-management functionality. It is also verifiable through review, automated testing, migration validation, and behavioral testing. Overall, completing this work will reduce ambiguity in future development and improve consistency between implementation and project requirements. 