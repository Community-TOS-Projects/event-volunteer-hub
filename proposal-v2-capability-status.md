# Current System Support for Unified Proposal v2.0

This document compares the capabilities in Unified Proposal v2.0 with the current Event Volunteer Hub application, which is the inherited MeetHub Django code.
It describes what exists today, not how missing features should be built.

## Capability Status

Capabilities are grouped by status:

- **Supported**: the capability exists and works.
- **Partially Supported**: some of the capability exists, but important parts are missing.
- **Not Yet Supported**: nothing in the application represents the capability.
- **Needs Clarification**: the requirement is too unclear to judge until it is discussed.

### Supported

- **Sign up and log in.** Users create an account and sign in with their email address (`accounts/urls.py`, `accounts/forms.py`).
- **Create and manage events.** Events can be created, viewed, edited, and deleted (`events/models.py`, `events/urls.py`). A fresh install has no event categories, so an admin must add one before events can be created (#11).
- **Open-source license.** The project is licensed under GPL-3.0 (`LICENSE`), and the inherited MIT notice is kept in `LICENSE-MIT`.

### Partially Supported

- **Log out.** A logout URL exists, but the logout link in the navigation menu is commented out (`events/base.html`). See #9.
- **User roles.** The proposal calls for administrator, coordinator, and volunteer roles. The application only has Django's built-in `is_staff` and `is_superuser` flags, and its `is_client` field is never used.
- **Server-side authorization.** Pages require login, but they do not check who owns what. Any signed-in user can edit or delete any event or comment by going to its URL directly. The edit and delete buttons are only hidden on the page.
- **Volunteer registration.** Users can mark themselves as "attending" an event. There are no shifts, no approval step, and no capacity limit.
- **Browsing events.** There is a list of events sorted by date and split across pages. There is no filtering, search, or calendar view.
- **Update notifications.** A site-wide activity feed shows actions such as "created a new event" (`actions/`). It shows every user's activity instead of only updates relevant to each user, and it can be viewed without logging in.
- **Relational database.** PostgreSQL is used when it is configured, and SQLite is used by default (`config/settings.py`). The database has no tables for organizations, shifts, or attendance.
- **Security.** Django provides password hashing and CSRF protection, and the ORM uses parameterized queries. The HTTPS cookie settings are not turned on, and the "attend" button changes data through a plain link (a GET request) instead of a form submission.
- **Minimal data collection and privacy.** The application collects only name, email, an optional date of birth, and an optional photo. However, any signed-in user can view any other user's profile, and photos are stored with a third-party service (Cloudinary).
- **Responsive design.** Pages use Bootstrap 4 and are set up for mobile screens. The event description editor has a fixed width of 970 pixels, which is wider than a phone screen.
- **Host-independent deployment.** A Dockerfile runs the application with Gunicorn. The app will not start without Cloudinary settings (#14), and the allowed hosts are hard-coded to `localhost` and `127.0.0.1`.

### Not Yet Supported

- **Password recovery.** There are no password reset pages, and no email service is configured.
- **Separate workspaces for each organization.** There is no organization model. Every user sees every event (`EventList` in `events/views.py`).
- **Sharing events between organizations.** This depends on organizations, which do not exist yet.
- **Shifts, volunteer positions, and capacity limits.** An event has a single date and time. There are no shift, position, or capacity fields.
- **Approval-based registration.** Registering adds the user immediately. There is no pending or approved state.
- **Coordinators assigning volunteers or tasks.** There is no assignment or task model.
- **Volunteer availability.** Volunteers have no way to enter their availability.
- **Volunteers viewing their own schedule.** The profile page lists events the user created, not events they are attending (`profile/views.py`).
- **Attendance check-in and service hours.** "Attending" only records that a user plans to come. Events have no duration, so hours cannot be calculated.
- **Email notifications.** An `email_user` method exists on the account model, but the application never calls it.
- **SMS messages.** Not present. The proposal lists SMS as optional.
- **Under-18 chaperone confirmation.** The profile has an optional date of birth field, but nothing uses it.

### Needs Clarification

- **Accessibility.** The templates contain very few accessibility attributes, and no accessibility review has been done. 

## Questions to Discuss Before Implementation For Clarification

1. What permissions does an administrator have that a coordinator does not?
2. Can a volunteer belong to more than one organization, and how are events shared between organizations?
3. Are "positions" and "tasks" the same thing? Does every event have shifts?
4. Is approval-based registration chosen per event or per organization?
5. Are service hours calculated from scheduled shift times or from check-in records?
6. Who confirms that a minor has a chaperone, and what information is stored?
7. Should update notifications be sent by email, shown in the app, or both?

