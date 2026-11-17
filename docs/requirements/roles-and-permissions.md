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
They create and manage events, shifts, and volunteer positions, manage volunteer sign-ups, assign volunteers, track attendance, and send event communications.
They do not manage user accounts or roles.

### Volunteer

A Volunteer takes part in events.
This is the default role for anyone who creates an account.
Volunteers browse events, sign up for or cancel their spot, manage their own profile and availability, and view their own schedule.

### Roles Across Organizations

Volunteer is the default role, but a user may not hold the same role everywhere.
The proposal gives each organization its own workspace, so in the future one user could be a Coordinator for Organization A and a Volunteer for Organization B.
If that is supported, a role belongs to a user within a specific organization, not to the user's account as a whole.
The permissions in this document should be read as "within a given organization."
For example, a user who is a Coordinator for Organization A would have Coordinator permissions only on Organization A's events, and Volunteer permissions on Organization B's events.
Whether this is supported is still undecided (see Q6).

## Permission Table

**Key:** Yes = allowed · No = not allowed · Own = only their own items · Q1, Q2, … = needs a decision (see Open Questions)

All permissions apply within a single organization (see Roles Across Organizations and Q6).

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
| 15 | Change a user's role | Yes | Q4 | No | Not available |
| 16 | Deactivate a user account | Yes | No | No | Command line only |
| 17 | Use the Django admin site | Q5 | No | No | Users with `is_staff` |
| 18 | Create and manage shifts and volunteer positions | Yes | Yes | No | Not available |
| 19 | Set capacity for an event, shift, or position | Yes | Yes | No | Not available |
| 20 | Assign volunteers to shifts or tasks | Yes | Yes | No | Not available |
| 21 | Manage availability | Own | Own | Own | Not available |
| 22 | View schedule | Own | Own | Own | Not available |
| 23 | View attendance and service-hour information | Yes | Yes | Own | Not available |
| 24 | Send and manage event communications or schedule updates | Yes | Yes | No | Not available |

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
15. **Change a user's role.** Not available. The app has no Administrator, Coordinator, or Volunteer roles yet, so there is no role to change. The `Account` model is not registered in the Django admin site (`meethub/accounts/admin.py` is empty), so accounts cannot be edited there either. The only related process is `python manage.py createsuperuser`, which creates a brand new account with `is_staff` and `is_superuser` set. It does not change the role or flags of an existing user. The only way to change an existing account's flags today is for a developer to edit them directly in the Django shell, which is a database edit and not a role-management feature.
16. **Deactivate a user account.** `Account.is_active` exists, but no page or admin screen changes it. It can only be changed by a developer in the Django shell.
17. **Use the Django admin site.** Any account with `is_staff` set can sign in at `/admin/`. Accounts made with `createsuperuser` get both `is_staff` and `is_superuser`.
18. **Create and manage shifts and volunteer positions.** Not available. An event has no shifts or positions. Volunteers can only sign up for the event as a whole.
19. **Set capacity.** Not available. There is no capacity field, and `attend_event` never checks a limit (see row 5).
20. **Assign volunteers to shifts or tasks.** Not available. There are no shifts or tasks to assign to, and no one can add another person to an event (see row 7).
21. **Manage availability.** Not available. The `Account` model and profile pages have no availability information.
22. **View schedule.** Not available. There is no schedule page or list of shifts for a user.
23. **View attendance and service-hour information.** Not available. The app does not record attendance (see row 10) or track hours.
24. **Send and manage event communications or schedule updates.** Not available. Comments on an event page are the only messages in the app, and they do not notify anyone or send email.

## Recommendation for `is_client`

**We recommend removing the `is_client` field from the `Account` model. This is a recommendation, not a final engineering decision, and it needs follow-up before any change is made.**

- **Nothing uses it.** It appears only in the model definition and in `REQUIRED_FIELDS` (`meethub/accounts/models.py`). No view, template, or form reads it.
- **It doesn't match any role.** The name comes from the original MeetHub project, and it does not correspond to Administrator, Coordinator, or Volunteer.
- **It can't represent three roles.** A true/false field can only tell two groups apart, so it is not a good starting point for the new roles.
- **It confuses setup.** Because it is in `REQUIRED_FIELDS`, `createsuperuser` asks every new contributor for a "Client status," and the README has to explain that it should be `False` and doesn't do anything.

**Follow-up needed:** the final decision belongs with the instructor, stakeholders, and the Architecture partnership as part of deciding how roles are stored. Before removing it, someone should confirm that no planned feature depends on it. Removing it would require a database migration and an update to the README's administrative access section.

## Open Questions

- **Q1. Can a Coordinator edit or delete any event in their organization, or only events they created?** (rows 3 and 4)
- **Q2. What volunteer information can each role see?** Can Volunteers see who else signed up for an event? Can Coordinators view the profile of any volunteer, or only volunteers signed up for their events? (rows 9 and 13)
- **Q3. Can a Coordinator delete other people's comments to moderate their events?** (row 12)
- **Q4. Can a Coordinator promote a Volunteer to Coordinator, or can only Administrators change roles?** (row 15)
- **Q5. Should the Administrator role be the same as Django's `is_staff` and `is_superuser` flags, with access to the Django admin site, or should it be a separate role inside the application?** (row 17)
- **Q6. Are roles assigned per organization?** The proposal gives each organization its own workspace. It is not yet decided whether one person can be a Coordinator in one organization and a Volunteer in another, or whether there is a site-wide Administrator above all organizations. This affects every row in the table. **This answer is critical.** If one user can hold different roles in different organizations (see Roles Across Organizations), roles cannot be stored as a single value on the user's account, and every permission check must know which organization it applies to. This should be decided before any role-based permissions are built.