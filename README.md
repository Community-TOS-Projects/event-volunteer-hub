# Event Volunteer Hub

Event Volunteer Hub is an open-source project for helping nonprofit organizations coordinate volunteers for short-term and community events.
The project is intended to support volunteer recruitment, scheduling, communication, roster management, and related event-coordination needs while remaining adaptable for different nonprofit workflows.

## Project Status

Event Volunteer Hub is under active development and is not currently a production-ready volunteer management system.
The project begins from an inherited event-management application and will be evaluated, stabilized, documented, and extended incrementally.

The repository was initialized from the open-source [MeetHub](https://github.com/iyanuashiri/meethub) project.
MeetHub provides an existing Django application foundation with user accounts, authentication, event creation, and other event-management capabilities.
Event Volunteer Hub is a separate project with a different purpose and development direction.

Some internal source-code names may continue to use `meethub` while the inherited application is evaluated.
Those names do not indicate that this repository is the original MeetHub project.

## Project Goals

The long-term project is intended to help nonprofit and community organizations:

- create and manage short-term community events;
- communicate volunteer opportunities and needs;
- coordinate volunteers, shifts, assignments, and rosters;
- identify filled and unfilled volunteer needs;
- reduce administrative work created by disconnected tools; and
- maintain an open-source system that future contributors can adapt and extend.

Development will proceed iteratively.
Not every long-term capability is implemented in the inherited codebase.

## Technology

The inherited application is built primarily with:

- Python
- Django
- HTML, CSS, Bootstrap, and JavaScript
- SQLite for local development

The inherited repository also includes configuration for additional deployment and cloud services.
Event Volunteer Hub deployment decisions will be documented separately as the project evolves.

## Local Development

### Prerequisites

- Python 3.10+
- `pip`
- Git
- `uv` if using the optional `uv` workflow

Clone the repository:

```bash
git clone https://github.com/Community-TOS-Projects/event-volunteer-hub.git
cd event-volunteer-hub
```

Copy the example environment file:

```bash
cp .env_example .env
```

Set a development `SECRET_KEY` in `.env`.
The inherited configuration can use SQLite for local development when external database settings are not supplied.

### Option 1: Python Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

### Option 2: uv

Install dependencies and create the environment:

```bash
uv sync
```

Run migrations:

```bash
uv run python manage.py migrate
```

Start the development server:

```bash
uv run python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Engineering Decisions

Significant engineering decisions are documented in the companion [Event Volunteer Hub Engineering Decision Log](https://github.com/Community-TOS-Projects/event-volunteer-edl).

The Engineering Decision Log records the context, rationale, alternatives, consequences, and follow-up work associated with important project decisions.
Contributors should review relevant EDL entries before changing an established project decision.

## Contributing

Event Volunteer Hub is developed through issues, branches, pull requests, review, and documented engineering decisions.
Contribution guidance will be maintained in `CONTRIBUTING.md`.

Before making a substantial change, review the open issues and relevant Engineering Decision Log entries so that new work builds on the existing project history.

## MeetHub Attribution

Event Volunteer Hub incorporates source code originally developed as [MeetHub](https://github.com/iyanuashiri/meethub).

MeetHub copyright:

> Copyright (c) 2018 Iyanu Ajao

The original MeetHub source was released under the MIT License.
The original MIT copyright and license notice are preserved in [`LICENSE-MIT`](LICENSE-MIT).

This repository was initialized by importing MeetHub source code without importing the original Git history.
The original MeetHub repository remains the authoritative source for its earlier development history.

## License

Event Volunteer Hub is distributed under the [GNU General Public License version 3](LICENSE).

Portions of the repository inherited from MeetHub remain subject to the original MIT copyright and license notice preserved in [`LICENSE-MIT`](LICENSE-MIT).
