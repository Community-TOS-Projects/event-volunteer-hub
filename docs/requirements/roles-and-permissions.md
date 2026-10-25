# Roles and Permissions

This document defines what the three roles in Unified Proposal v2.0 (Administrator, Coordinator, and Volunteer) are allowed to do.
It also records what the current application allows today, so contributors can see the gap.
It describes requirements, not how they should be implemented.

## Roles

### Administrator

An Administrator manages an organization's workspace.
They can do everything a Coordinator can do, and they also manage users, roles, and organization-wide settings such as event categories.
The proposal says administrators get "more detailed controls" than other users.

### Coordinator

A Coordinator runs events.
They create and manage events, manage volunteer sign-ups, assign volunteers, and track attendance.
They do not manage user accounts or roles.

### Volunteer

A Volunteer takes part in events.
This is the default role for anyone who creates an account.
Volunteers browse events, sign up for or cancel their spot, manage their own profile and availability, and view their own schedule.

## Permission Table

**Key:** Yes = allowed · No = not allowed · Own = only their own items · Q1, Q2, … = needs a decision (see Open Questions)

| # | Action | Administrator | Coordinator | Volunteer | Current app |
| --- | --- | --- | --- | --- | --- |
| 1 | View events | Yes | Yes | Yes | Any signed-in user |
| 2 | Create an event | Yes | Yes | No | Any signed-in user |
| 3 | Edit an event | Yes | Q1 | No | Any signed-in user |
| 4 | Delete an event | Yes | Q1 | No | Any signed-in user |
| 5 | Sign up for an event | Yes | Yes | Yes | Any signed-in user |
| 6 | Cancel their own sign-up | Yes | Yes | Yes | Any signed-in user |
| 7 | Add or remove another person's sign-up | Yes | Yes | No | Not available |
| 8 | Approve or reject sign-ups | Yes | Yes | No | Not available |
| 9 | See who signed up for an event | Yes | Yes | Q2 | Any signed-in user (count only) |
| 10 | Record attendance | Yes | Yes | No | Not available |
| 11 | Post a comment | Yes | Yes | Yes | Any signed-in user |
| 12 | Delete a comment | Yes | Q3 | Own | Any signed-in user, any comment |
| 13 | View another user's profile | Yes | Q2 | No | Any signed-in user |
| 14 | Manage event categories | Yes | No | No | Staff, through the Django admin site |
| 15 | Change a user's role | Yes | Q4 | No | Command line only |
| 16 | Deactivate a user account | Yes | No | No | Command line only |
| 17 | Use the Django admin site | Q5 | No | No | Users with `is_staff` |

## What the Current Application Allows

Each item below matches a row in the table and can be checked in the code.

1. **View events.** `EventList` requires login and returns every event to every user (`meethub/events/views.py`).
2. **Create an event.** `EventCreate` only requires login, so any signed-in user can create an event.
3. **Edit an event.** `EventUpdate` only requires login, so any signed-in user can edit any event by going to `/events/<id>/update`. The Edit button is shown only to the event's creator, but the page itself is not protected (`events/detail.html`). Editing also makes the editor the event's new creator, because `EventFormMixin` sets `creator` to the current user every time the form is saved.
4. **Delete an event.** `EventDelete` only requires login, so any signed-in user can delete any event by going to `/events/<id>/delete`.
5. **Sign up for an event.** `attend_event` adds the user to the event immediately. There is no approval step or capacity limit.
6. **Cancel their own sign-up.** `not_attend_event` removes the user from the event.
7. **Add or remove another person's sign-up.** No page or view does this. The Django admin form for events does not include the attendee list (`meethub/events/admin.py`).
8. **Approve or reject sign-ups.** Not available. Sign-ups take effect immediately.
9. **See who signed up.** Any signed-in user can see the attendee section on an event page. It shows the number of attendees, but the names come out blank because the template uses `attendee.username`, which the `Account` model does not have (`events/detail.html`).
10. **Record attendance.** Not available. The app only records that someone plans to attend.
11. **Post a comment.** Any signed-in user can comment on or reply to any event (`EventDetail` and `comment_detail`).
12. **Delete a comment.** `CommentDelete` only requires login, so any signed-in user can delete any comment by going to `/comments/<id>/delete/` (`meethub/comments/views.py`).
13. **View another user's profile.** `UserDetail` only requires login, so any signed-in user can view any profile (`meethub/profile/views.py`).
14. **Manage event categories.** Categories can only be added in the Django admin site, which requires `is_staff` (`meethub/events/admin.py`).
15. **Change a user's role.** There is no page for this. The `Account` model is not registered in the Django admin site (`meethub/accounts/admin.py` is empty), so roles can only be changed with `createsuperuser` or the Django shell.
16. **Deactivate a user account.** Same as row 15. `Account.is_active` exists, but there is no page that changes it.
17. **Use the Django admin site.** Any account with `is_staff` set can sign in at `/admin/`. Accounts made with `createsuperuser` get both `is_staff` and `is_superuser`.

## Recommendation for `is_client`

**Remove the `is_client` field from the `Account` model.**

- **Nothing uses it.** It appears only in the model definition and in `REQUIRED_FIELDS` (`meethub/accounts/models.py`). No view, template, or form reads it.
- **It doesn't match any role.** The name comes from the original MeetHub project, and it does not correspond to Administrator, Coordinator, or Volunteer.
- **It can't represent three roles.** A true/false field can only tell two groups apart, so it is not a good starting point for the new roles.
- **It confuses setup.** Because it is in `REQUIRED_FIELDS`, `createsuperuser` asks every new contributor for a "Client status," and the README has to explain that it should be `False` and doesn't do anything.

Removing it requires a database migration and an update to the README's administrative access section.
How the new roles are stored should be decided separately.

## Open Questions

- **Q1. Can a Coordinator edit or delete any event in their organization, or only events they created?** (rows 3 and 4)
- **Q2. What volunteer information can each role see?** Can Volunteers see who else signed up for an event? Can Coordinators view the profile of any volunteer, or only volunteers signed up for their events? (rows 9 and 13)
- **Q3. Can a Coordinator delete other people's comments to moderate their events?** (row 12)
- **Q4. Can a Coordinator promote a Volunteer to Coordinator, or can only Administrators change roles?** (row 15)
- **Q5. Should the Administrator role be the same as Django's `is_staff` and `is_superuser` flags, with access to the Django admin site, or should it be a separate role inside the application?** (row 17)
- **Q6. Are roles assigned per organization?** The proposal gives each organization its own workspace. It is not yet decided whether one person can be a Coordinator in one organization and a Volunteer in another, or whether there is a site-wide Administrator above all organizations. This affects every row in the table.
