# Worklog - 11-13-26 copies prior # Work Log - 2026-11-02

Temporary record of the debugging and code changes made during this session. This file is separate from `README.md` and is intended to be removed later.

## Project Context

- This is a Django event management project. The default SQLite database is `db.sqlite3` in the repository root.
- The configured authentication model is `accounts.Account`; it uses `email` as `USERNAME_FIELD` and has no `username` field.
- `Account.__str__()` delegates to `get_fullname()`, which formats the name as `Last First`.
- Event time fields were changed from the old `time` field to `start_time` and `end_time`. Shifts have datetime start/end values and validation against the parent event's date/time range.

## Earlier Work Covered In This Session

- Identified the database location and explained that shift-related models belong under `meethub/events/models.py`. At the time the location question was asked, the user explicitly requested guidance only, not implementation.
- Aligned event code with the current schema in forms, views, admin, templates, and tests: event `time` references were replaced with `start_time` / `end_time` where covered.
- Updated event admin displays and lookup paths for the custom account model. `user__email` is a valid relation traversal from a related `Account`; `username` is not an `Account` field.
- Updated event form fields/help text and the event detail/list/delete templates to use the current time fields.
- Updated event tests to construct custom accounts with email, use email-based login, and use the current event time fields.
- Explained that Django tests should be run with `python manage.py test ...` in the project's virtual environment.
- The event form test module had previously been reported as passing (11 tests).

## Event View Test Failures And Changes

The supplied `test_views` traceback reported 11 errors. The identified causes and changes were:

- `EventCreate` specified both `form_class = EventForm` and `fields`. Removed the view-level `fields`; `EventForm.Meta.fields` defines those fields.
- `delete.html` was missing closing template/style tags. Added `</style>` and `{% endblock %}`.
- `EventDelete` used `SuccessMessageMixin` with `%(name)s`, but the confirmation form has no `name` in `cleaned_data`. Removed that mixin and added a `form_valid` implementation that captures the event name before deletion, then emits the success message.
- `CommentCreate` attempted to get an object from a create view and tried to record an activity before the comment was saved. It now fetches the event from the detail route's `pk` using Django's `get_object_or_404`, assigns the event and logged-in user, saves through the generic create flow, then records the activity. Its success URL uses the saved comment's event ID.
- Updated the comment POST test to submit the comment field, changed deprecated `assertEquals` to `assertEqual`, and changed the expected delete redirect to the named event-list URL.
- Corrected account string assertions to match `get_fullname()` (`Last First`).
- The user subsequently reported that `meethub.events.tests.test_views` ran without errors. A focused attendee-rendering test was also run successfully by Copilot after the latest template change; the full view module was not independently confirmed by Copilot after all final changes.

## Attendance Test Clarification

- `meethub/events/tests/test_attendance.py` is in the events app, not the accounts app.
- It tests the event attendee workflow: attending/leaving through views and the `Event.attendees` many-to-many relation.
- The separate `Attendance` model in `meethub/events/models.py` stores a user/event/optional shift, status, and hours. The user noted that model-focused coverage is in `meethub/events/tests/test_models.py`.
- The attempt to run `test_attendance.py` was skipped/cancelled, so that module's current test result is unverified.

## Factory And Attendee Template Changes

- Updated `EventFactory` in `meethub/events/factories.py`: replaced the removed `time` field with `start_time` and `end_time`, and changed the date default to a callable `date.today` for `factory.LazyFunction`.
- Changed the attendee display in `meethub/events/templates/events/detail.html` from `attendee.username` to `attendee.get_fullname`, matching the custom account model.
- Strengthened the event detail test to add an attendee and assert that the attendee's full name appears in the response.
- Added `test_event_factory_uses_current_time_fields` to `meethub/events/tests/test_models.py`.
- Corrected Factory Boy's Django base class from `factory.DjangoModelFactory` to `factory.django.DjangoModelFactory` in `meethub/accounts/factories.py`, `meethub/comments/factories.py`, and `meethub/events/factories.py`.
- The initial error was not caused by a missing `factory-boy` install: version 3.3.3 was installed. The incorrect API path caused `AttributeError: module 'factory' has no attribute 'DjangoModelFactory'` when test discovery imported `EventFactory` and transitively `AccountFactory`.
- A temporary factory-test import was removed while investigating the error, then restored after correcting all factory base classes; the regression test now runs.

## Validation Performed

- Passed: focused `EventFactory` schema regression test plus event detail attendee rendering test (2 tests total).
- Passed: full `meethub.events.tests.test_models` module (28 tests) before adding cascade and time-boundary coverage.
- Passed: the three cascade-deletion tests individually, then the full `meethub.events.tests.test_models` module (31 tests).
- Passed: `AttendanceModelTest.test_shift_cannot_cross_midnight` (1 test); confirms a Shift ending on the following date is rejected.
- Passed: the three focused Event end-time and Shift overlap tests.
- Passed: full `meethub.events.tests.test_models` module after the PR 27 event-time and shift-overlap validation changes (35 tests).
- Static diagnostics reported no errors in the edited event factory/test files at the time checked.
- The test runner emitted an existing warning during a view test about no `static/` directory; it did not fail the focused test.
- No complete project-wide test run was performed.

## Remaining Checks / Known Gaps

- Full `meethub.events.tests.test_views` was reported passing by the user, but was not captured as a complete final run by Copilot after the most recent edits.
- `meethub.events.tests.test_attendance` was not run.
- A later targeted search found no remaining old `Event.time` references or Account `username` property lookups in the events/accounts folders. The `form.username` references in the accounts login template are Django authentication-form fields and are valid with email-based authentication.
- The repository-wide search found other legacy username/time assumptions outside the event/accounts folders, including comments/profile/action tests. Those files were not updated in this pass and remain a consideration for a later cleanup.
- `meethub/comments/factories.py` still has its own date/time `factory.LazyFunction(...)` expressions to review; only its Factory Boy Django base class was corrected here.
- Historical event migrations still mention the old `time` field by design; migration history should not be rewritten for this cleanup.

## Maintainer Feedback Tracker

- [x] Rename the Event `time` field to `start_time` and add `end_time`; update forms and related event references. Completed in the current event/account scope.
- [OOS] Organization is intended as the host-name reference for Events; defer relationship implementation because it requires a coordinated, broader edit to the Account model and accounts folder. See the deferred proposal section below.
- [OOS] Organization behavior is still an open question; defer PR/design resolution until the required accounts-folder work is in scope.
- [ ] Check for misalignment with PR #27; exact comparison remains to be done.
- [x] Decide whether a Shift may exist outside its Event's time range. No; keeping shifts within the Event's time range is intentional and current validation enforces it.
- [x] Decide whether an Event may omit its end time. No; Events must have an end time and the current model/form require it.
- [~] Decide how cross-midnight work should be represented. User intent: Events are same-day and a Shift must not cross midnight; if work continues on a new day, use a separate shift. Current validation rejects a crossing shift, but the same-day Event bound means a next-day shift cannot belong to that same Event; clarify whether the continuation should be a separate Event.
- [ ] Create an EDL documenting implementation decisions defined by other project documentation; this can be done in Week 12.
- [x] Add deletion tests: deleting an Event deletes its Shifts; deleting an Event deletes associated Attendance rows; deleting a volunteer Account deletes that volunteer's Attendance rows. All three targeted tests and the full event model test module pass.
- [x] Fix the Django admin `userusername` typo. The lookup now uses the related Account's email field (`user__email`).
- [~] Clarify the intentional overlap between `Event.attendees`, `Shift.volunteers`, and `Attendance`; working interpretation recorded below, with detailed invariants still to confirm.

### Relationship Design Note

The relationships are intentionally related but serve different workflow stages; avoid removing one solely because the same Account may appear in more than one:

- `Event.attendees`: event-level RSVP / intent to attend, independent of a particular shift.
- `Shift.volunteers`: assignment of an Account to provide volunteer coverage for a specific shift; Shift capacity applies here.
- `Attendance`: a status-and-hours record for an Account at an Event, optionally associated with a Shift. This can represent approval, actual attendance, cancellation, and recorded hours rather than just signup.

This separation explains the intended overlap, but code-level consistency rules remain open: for example, whether assigning a volunteer to a Shift must also add them to `Event.attendees`, whether an `Attendance.shift` must belong to its `Attendance.event`, and whether event-level Attendance without a Shift is supported. Clarify these decisions before changing the schema or synchronizing the relationships automatically.

The code review confirmed that the event attend/leave views currently update only `Event.attendees`; no application workflow currently assigns `Shift.volunteers` or creates `Attendance` rows. The three concepts are intentionally distinct in this design discussion, but their lifecycle and cross-relation invariants still need an explicit product decision. The three cascade tests requested by the maintainer have been added to `AttendanceModelTest` and verified as passing.

### Event Time Decision Notes

- Shifts must remain within the Event's time range; this is an intentional rule and is enforced by `Shift.clean()` / `Shift.save()` with model-test coverage for in-range and out-of-range shifts.
- Events must have an end time; this is intentional and enforced by the non-nullable `Event.end_time` field and required `EventForm` field.
- Event stores one `date` plus separate `start_time` and `end_time` values. Shift validation combines both event times with that same date and has no next-day rollover handling. `AttendanceModelTest.test_shift_cannot_cross_midnight` passes and verifies a Shift crossing midnight is rejected. The user intends to avoid overnight shifts; clarify whether work continuing the next day is a separate Event, since current same-day bounds prohibit a next-day Shift on the same Event.

### Organization Design Note

The intended purpose clarified by the user is to use `Organization` as the host-name reference for an Event. An Account creates the Event, and the Account's email is the means of identifying who created it. Implementing this requires a coordinated, broader edit to the Account model and accounts folder to represent account membership in an Organization. The relationship implementation and related Organization behavior feedback are out of scope until that work is scheduled; no Organization relationships or schema changes are currently accepted.

### Deferred Organization Relationship Proposals

Two possible implementations were discussed but are not accepted yet. Both remain out of scope until the required accounts-folder work is finalized:

1. `Organization.owner` points to an Account, while `Event.organization` points directly to its host Organization. This records ownership and hosting separately, but the owner direction/cardinality did not match the user's intended model.
2. `Account.organization` points to an Organization, allowing many Accounts per Organization. An Event's host would then be derived through `Event.creator.organization`, avoiding a duplicate direct Event-to-Organization link. This better matches the clarified intent, but is still deferred until other maintainer feedback and design questions are finalized.

The exploratory code and migration for these relationships were removed. The current model remains unchanged: Organization is standalone, and Event creator remains an Account relation. Revisit this section before implementing the host lookup or showing a host organization in event/email output.
_____________________________________________________________________________________________________



## Align Volunteer Participation Models with PR27 and PR39 Requirements

This is the planned data-model and relationship redesign described in the Build Day issue added to `PR_REFERENCE.md`. No implementation has started. The goal is to align the current PR29 participation models with the distinct domain concepts and workflows defined by PR27 and PR39.

### Current Problem

- The current schema has `Event.attendees`, `Shift.volunteers`, and `Attendance`, but their responsibilities do not fully match the requirements.
- `Shift.volunteers` is a direct many-to-many relation and therefore acts as an implicit assignment/sign-up mechanism without preserving sign-up status or history.
- `Attendance` currently has `pending`, `approved`, `attended`, and `cancelled` statuses, mixing sign-up/approval-like states with an attendance record that should hold attendance status and hours only.
- RSVP, Sign-Up, Assignment, and Attendance need distinct, documented roles and relationships.

### Planned Responsibilities

- **RSVP:** represent event-level intent to attend, independent of volunteering for a shift.
- **Sign-Up:** represent a volunteer's request for a particular shift and its lifecycle state: `pending`, `confirmed`, `declined`, or `cancelled` (PR39 vocabulary). A volunteer may request multiple shifts in one event but must not have duplicate active sign-ups for the same shift.
- **Assignment:** represent confirmed scheduling of a volunteer to a shift, separately from RSVP and attendance. Determine whether it remains a distinct record after sign-up approval.
- **Attendance:** represent attendance-specific status and recorded hours for an event, optionally associated with a shift from that same event. It must not manage sign-up approval states.
- **Capacity:** pending and confirmed sign-ups reserve event and shift capacity; cancellation releases the reserved spot. Enforce finite positive event and shift limits against distinct participants. A person who RSVPs and volunteers counts once toward event capacity; shift capacity counts distinct volunteers assigned to that shift.

### Planned Work

1. Compare the current PR29 models, relationships, and usages against the PR27/PR39 definitions.
2. Decide and document the separate database responsibilities and lifecycle for RSVP, Sign-Up, Assignment, and Attendance.
3. Design any required model/relationship changes, including whether `Shift.volunteers` must be replaced or redesigned.
4. Define the necessary schema migrations and how existing Attendance data/statuses are handled.
5. Refactor affected relationships and application endpoints/business logic so they no longer conflate RSVP, Sign-Up, Assignment, and Attendance.
6. Update model tests and relationship documentation; add automated tests for the revised relations and workflows.
7. Verify required migrations apply and existing event/shift regression tests still pass.
8. Record deferred architecture concerns for follow-up.

### Acceptance Checks

- RSVP is represented separately from volunteer Sign-Up.
- Sign-Up has the agreed lifecycle states and prevents duplicate active requests for one volunteer/shift.
- Assignment is distinguishable from RSVP and Attendance, with the post-approval relationship explicitly documented.
- Attendance stores attendance-specific information only.
- `Shift.volunteers` no longer serves as an undocumented substitute for Sign-Up or Assignment.
- The relationships are distinguishable in the schema and documented.
- Migrations apply successfully, focused relationship/workflow tests pass, and existing event/shift regression tests pass.
- Deferred concerns are documented rather than expanded into this implementation.

### Out Of Scope

- Organization-to-Account and Organization-to-Event relationships.
- Existing event end-time migration strategy.
- Coordinator role implementation.
- Email notification workflows.
- Waitlist functionality.
- Volunteer Position and Task assignment workflows.
- Frontend Sign-Up, RSVP, or Attendance interfaces.

### Unresolved Decisions

These questions must remain open until the team confirms answers; implementation must not silently assume them:

- Legacy Attendance rows with sign-up statuses but nonzero recorded hours must be manually reviewed before migration; the local database has zero Attendance rows, and broad cross-environment inventory is not the current priority.

### Sign-Up And Assignment Decision

PR39 says a confirmed Sign-Up becomes an Assignment. The user has chosen that model: the Sign-Up record itself becomes the Assignment when its status changes to `confirmed`; a separate Assignment row will not be added for this implementation. When a no-shift reserve is placed on a Shift, update the existing Sign-Up's optional `shift` field rather than creating a second Sign-Up. In approval mode, approving/placing a pending reserve makes it `confirmed` and attaches the Shift; in direct mode, the reserve is already confirmed, so placement only attaches the Shift. This avoids duplicate volunteer/shift relations while preserving the original request record and its lifecycle status.

### Attendance And Shift-Volunteer Data Migration Plan

Proceed with a data-preserving migration for the existing local schema:

- `Attendance.pending` becomes `SignUp.pending`.
- `Attendance.approved` becomes `SignUp.confirmed`.
- `Attendance.cancelled` becomes `SignUp.cancelled` and remains as sign-up history.
- `Attendance.attended` remains an Attendance record with its hours preserved.
- Preserve each migrated record's Account, Event, optional Shift, and timestamps where available. A null Shift becomes an event-level reserve Sign-Up.
- Convert each existing `Shift.volunteers` relation into a `SignUp.confirmed` for that Account, Event, and Shift. Avoid creating a duplicate active Sign-Up if one was already migrated from Attendance.
- If a pending/approved/cancelled Attendance row has nonzero `hours_recorded`, stop for manual review or preserve the hours separately; do not silently discard or reinterpret them.

The local database currently has no Attendance rows. Other environments are not the immediate focus, but the migration must fail safely on ambiguous nonzero-hour rows rather than lose their data.

### Decisions Confirmed So Far

- Use PR39's sign-up statuses: `pending`, `confirmed`, `declined`, and `cancelled`. Treat the Build Day wording `approved` as the action that transitions a request to `confirmed`, not as a separate stored status.
- Pending sign-ups reserve capacity from the start. Confirmed sign-ups continue to count. Cancelling a sign-up releases its reserved spot.
- For Event capacity, count distinct people across RSVP and sign-up participation; one person who RSVPs and signs up for one or more shifts counts once, as required by PR27/PR39.
- Event capacity must always be positive; a newly created Event may have zero current RSVP attendees. Current attendee count comes from the `Event.attendees` relation and is independent of the capacity limit.
- A confirmed no-shift reserve Sign-Up counts once toward Event capacity but not toward any Shift capacity; once assigned to a Shift, it counts toward that Shift as well, without counting the person twice toward the Event limit.
- When a reserve is assigned to a Shift, update the existing Sign-Up's `shift` rather than create a duplicate Sign-Up. In approval mode, the pending-to-confirmed transition occurs with approval/placement; a direct-mode reserve is already confirmed.
- Shift capacity counts volunteers with pending or confirmed sign-ups for that shift; final declined and cancelled sign-ups release capacity.
- Direct sign-up is the default and confirms immediately when there is capacity; a coordinator may choose approval-based sign-up per event.
- A volunteer may Sign-Up for an Event without selecting a Shift, including as an unassigned reserve even when the Event has shifts. The reserve is still a Sign-Up, not an RSVP; the same Account may separately RSVP, and event capacity counts that person only once.
- `Event.attendees` remains the RSVP relation and its current count is derived from that relation; it is not capacity. Rename the legacy `Event.num_of_attendees` field to `Event.capacity` as the maximum number of distinct participants, preserving meaningful non-zero values.
- A zero legacy value means capacity was unset, not that the Event had zero participants or a valid zero capacity. Manually backfill every pre-migration Event with a positive capacity before enforcing the required positive limit. This applies to any Event created under the old code, whether local or imported; newly created Events must provide a positive capacity. A coordinator can handle legacy backfill when coordinator roles exist.
- Attendance-specific statuses should include `attended` and `absent`; Sign-Up approval states belong to Sign-Up, not Attendance.

### Event Capacity Migration Decision
The user’s confirmed data meaning is:

- `capacity` is a maximum and must be a positive integer in the completed PR27 design.
- An Event may start with zero RSVP attendees; that state is represented by an empty `Event.attendees` relation and a computed count of zero.
- A legacy value of `num_of_attendees = 0` means “capacity not set,” not “zero attendees” and not a valid zero capacity.
- Meaningful nonzero legacy capacity values should be preserved, subject to data inspection.
- Any Event created before the schema change is legacy, including Events created by the team; “legacy” does not mean only imported Events.

#### Chosen Transition: Nullable Placeholder, Then Manual Backfill

Use a staged migration rather than inventing a capacity:

1. Rename `num_of_attendees` to `capacity`, preserving existing nonzero values. Convert legacy zeros to `NULL` to represent “unset.” The migration may temporarily allow null only for legacy rows.
2. Require a positive capacity for all newly created Events through the form/model validation. Do not add a default capacity of `1` for new Events; organizers must set the intended maximum.
3. Keep legacy Events with `capacity = NULL` out of RSVP/sign-up capacity acceptance until an authorized person manually enters their actual positive capacity. This is a migration exception, not the final PR27 rule.
4. Inventory and manually backfill every legacy null capacity in each relevant database/environment. The local database had zero Event rows when checked; other environments still need inspection. Once coordinator roles exist, this can be assigned to a coordinator; until then an authorized administrator/person must perform it.
5. After no null capacities remain, make the field non-nullable and enforce `capacity >= 1` at model and database levels. At that point every Event satisfies PR27's finite positive capacity requirement.

The `NULL` placeholder is deliberately temporary. It allows schema deployment without pretending an unknown limit is `1`, while making the missing capacity explicit. Code must fail closed for an Event whose capacity remains unset; it must not treat null as unlimited.

#### Alternative Considered: Backfill Zeros To One

Automatically changing every legacy zero to `1` would make the migration immediately satisfy the positive constraint and let schema deployment continue. However, it would invent a limit that may not match the real Event, could constrain participation to one person if enforcement is enabled before manual correction, and would make a placeholder indistinguishable from an intentional capacity of one unless an additional review marker were added. A permanent model default of `1` would also silently limit all newly created Events to one participant. For these reasons, automatic `1` is rejected as the data meaning; the staged null-and-manual-backfill approach is preferred.

#### Alternative Considered: Require Manual Backfill Before Migration

Requiring every database to be manually corrected before deploying any migration avoids a nullable transition, but blocks schema deployment until all environments and rows are inventoried. The staged null approach allows deployment while explicitly identifying records that still need attention, then tightens the schema after backfill.

### Scope Priority Update

The user has clarified that PR 27 should be completed first as the foundation required by PR 39. This priority supersedes the earlier Build Day note's narrower exclusions for requirements explicitly in PR 27. The implementation target now includes:

- Event end time later than event start time, with events and shifts on the same date.
- Shift containment within its Event and non-overlap between shifts in the same Event.
- Separate finite positive Event and Shift capacities, enforced against distinct participants and assignments.
- Attendance records optionally linked to a Shift only when that Shift belongs to the same Event.
- Separate RSVP, Sign-Up, Assignment, and Attendance responsibilities per PR 27/39.
- Sign-Up may be event-level with no Shift (reserve), or tied to one specific Shift. A no-shift reserve may later be assigned; the recommended design is to update the same Sign-Up with its Shift, pending confirmation.

Organization relationships, frontend workflows, coordinator roles, email notifications, waitlists, and Position/Task workflows remain out of scope. PR27 Event end-time ordering and Shift containment/non-overlap validation have been implemented and the event model suite passes; the participation-model redesign, Event capacity rename, and migrations remain to be done. Existing Attendance data migration still needs discussion.

### Reference And Implementation Notes

- PR39 refers to `event-shifts.md`, but that file was not found in the workspace during review. Confirm its location or add it before relying on it as an additional authority.
- The Unified Proposal v2.0 PDF is present under `docs/`; PR_REFERENCE cites it as the source for proposal sections. Consult the cited sections during design.
- Keep this work at the data-model/relationship-design boundary. Do not implement the excluded user interfaces, coordinator roles, notifications, waitlisting, Position/Task workflows, or organization relationships as part of this issue.

### Clarification Added 2026-11-13

- `pending` means awaiting coordinator review and reserves event and shift capacity.
- `confirmed` sign-ups continue to count toward event and shift capacity.
- Final `declined` and `cancelled` sign-ups remain stored for history but release capacity.
- Event capacity counts each distinct person once across RSVP and sign-up participation; shift capacity counts pending or confirmed sign-ups for that shift.
- Direct sign-up is the default and confirms immediately when there is capacity. A coordinator may choose approval-based sign-up for an event; those requests start as pending for review.
- PR39 Q7 is resolved: volunteers may Sign-Up for an Event with no Shift and be held as an unassigned reserve; this does not create an RSVP. Event capacity counts the person once if they also RSVP or Sign-Up for shifts.
- An unassigned reserve counts toward Event capacity only; once assigned to a Shift, it counts toward that Shift's capacity and remains one distinct Event participant.
- PR39's status vocabulary is `pending`, `confirmed`, `declined`, and `cancelled`; treat Build Day's `approved` wording as the action that transitions a sign-up to `confirmed`, not as an additional status.
- The confirmed Sign-Up itself becomes the Assignment; no separate Assignment row is planned initially. Existing Attendance-data migration remains undecided; consider data in environments other than the local database.

Participation Model Redesign Completed

Implemented the Architecture & Data redesign required by PR27, PR39, and maintainer feedback.

Event Model Changes
Replaced legacy num_of_attendees field with capacity.
Preserved legacy database values by using a migration RenameField rather than deleting and recreating the field.
Added Event capacity validation.
Added signup_mode field to support:
direct
approval
Added participant counting logic that combines RSVP and Sign-Up participation without double-counting users.
Shift Model Changes
Removed Shift.volunteers ManyToMany relationship.
Volunteer participation is now represented through the SignUp model.
Shift capacity validation remains enforced.
Shift overlap validation remains enforced.
SignUp Model Added

Created a new SignUp model to represent volunteer participation independently from RSVP and Attendance.

Implemented statuses:

pending
confirmed
declined
cancelled

Implemented rules:

Pending and confirmed sign-ups reserve capacity.
Declined and cancelled sign-ups remain in history but no longer consume capacity.
Reserve sign-ups without a shift are supported.
Confirmed SignUps serve as the assignment record (no separate Assignment model).
Attendance Model Refactor

Attendance was redesigned to store attendance information only.

Removed workflow-related statuses:

pending
approved
cancelled

Attendance now supports:

attended
absent

Added validation ensuring an Attendance shift belongs to the same Event.

Test Suite Updates

Updated Events application tests to reflect the redesigned schema:

Event Model Tests: Passing
Event Views Tests: Passing
Attendance Tests: Passing

Updated:

Event creation tests to provide required capacity values.
Factory definitions to use capacity instead of num_of_attendees.
Attendance tests to use attendance-specific statuses.
Form tests to include Event capacity requirements.
Migrations

Successfully applied:

Plain Text
events.0015_remove_event_num_of_attendees_and_more
events.0016_alter_attendance_status_alter_event_capacity

Migration verification completed successfully.

Current Status

All tests within the meethub.events application are passing.

The PR27/PR39 participation-model redesign has been implemented within the agreed Architecture & Data scope.