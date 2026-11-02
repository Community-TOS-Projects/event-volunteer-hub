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
| Term | Meaning | How it relates to shifts |
|------|---------|--------------------------|
| **Shift** | A block of time within an event (defined in `event-shifts.md`). | This is what a volunteer signs up for. |
| **Position** | A role with its own spot limit, like "Greeter" or "Food Server." (§3) | A position sits inside a shift. One shift can have several positions. |
| **Task** | A specific job a coordinator gives a volunteer who is already signed up, like "Restock the water table." (§1, §3) | Tasks happen during a shift. Volunteers do not sign up for tasks. |

## Requirements

| # | Requirement | Proposal source | Open question |
|---|-------------|-----------------|---------------|
| R1 | Volunteers sign up for a **shift**, not a whole event. | §1, §3 | Q1 (positions) |
| R2 | A volunteer cannot sign up for the same shift twice. | §4 Database | |
| R3 | **Direct sign-up:** the volunteer is confirmed right away if there is room. | §3 | |
| R4 | **Approval sign-up:** the sign-up is "pending" until a coordinator approves or declines it. | §3 | Q2 (who decides), Q3 (do pending sign-ups hold a spot) |
| R5 | A coordinator, not the volunteer, picks which type of sign-up an event uses. | §3, §4 Back End | Q2 |
| R6 | Each sign-up has a status: pending, confirmed, declined, or cancelled. | §3, §4 Database | Q4 (waitlisted status) |
| R7 | **When a shift is full,** new sign-ups are blocked and the volunteer sees that it is full. | §1, §4 Database | Q4 (waitlist) |
| R8 | The spot limit is enforced by the server, so two people cannot take the last spot. | §4 Database | |
| R9 | A volunteer can cancel their own sign-up. Cancelling frees the spot. | §1, §3 | Q5 (cutoff time) |
| R10 | A cancelled sign-up is kept with status "cancelled," not deleted, so volunteer hour records stay accurate. | §3 | |
| R11 | Volunteers get an email when they are confirmed, approved, or declined. | §3, §4 Communication | |
| R12 | Volunteers under 18 may need a chaperone confirmation before they are confirmed. | §3, §7 Assumptions | Q6 |

## Open questions
- **Q1.** Are positions part of the first version, or added later?
- **Q2.** Who counts as a coordinator, and is approval set per event or per shift?
- **Q3.** Does a pending sign-up hold a spot while it waits for approval?
- **Q4.** When a shift is full, do we only block sign-ups, or also offer a waitlist?
- **Q5.** Can volunteers cancel at any time, or is there a cutoff (for example, 24 hours before)?
- **Q6.** Does the under-18 chaperone check happen before, after, or instead of coordinator approval?
