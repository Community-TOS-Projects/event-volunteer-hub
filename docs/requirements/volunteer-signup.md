# Volunteer Sign-Up Requirements

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
