# CampusFlow — Team 07

CampusFlow is a Python project for managing campus IT support tickets. It helps record issues, calculate their priority, and assign them to staff.

## Current features

- Create tickets with validated titles, categories, urgency, and affected-user counts.
- Generate sequential ticket IDs such as `T001` and `T002`.
- Calculate priority from urgency and the number of affected users.
- List tickets and retrieve a ticket by ID.
- Assign an existing ticket to a staff member.
- Run automated tests with Python's built-in `unittest` module.

Tickets currently live in a list of dictionaries in memory. The repository does not yet include a runnable CLI or persistent storage.

## Requirements

- Python 3.8 or later
- Git to clone the repository

The current modules and tests use the Python standard library; no third-party packages are required.

## Setup

```bash
git clone https://github.com/sounegbe/CampusFlow-team-07.git
cd CampusFlow-team-07
python3 --version
```

Run the commands below from the repository root. On Windows, use `py` instead of `python3` if needed.

## Try it

Start the Python interpreter:

```bash
python3
```

Then create and assign a ticket:

```python
from campusflow.tickets import create_ticket, get_ticket, list_tickets
from campusflow.workflow import assign_ticket

tickets = []

ticket = create_ticket(
    tickets,
    title="Campus Wi-Fi is down",
    category="Network",
    urgency="high",
    affected_users=25,
)

print(ticket["id"])        # T001
print(ticket["priority"])  # critical

assign_ticket(tickets, ticket["id"], "Ada")

print(get_ticket(tickets, "T001")["assigned_to"])  # Ada
print(list_tickets(tickets))
```

Exit the interpreter with `exit()`. In-memory tickets are lost when the Python process ends.

## Validation and priority

Ticket creation accepts:

| Field | Rule |
| --- | --- |
| Title | Nonblank text; surrounding whitespace is removed |
| Category | Network, Hardware, Software, or Other; case-insensitive |
| Urgency | low, medium, or high; case-insensitive |
| Affected users | A positive integer; booleans are rejected |

Invalid ticket input raises `ValueError`.

Priority rules are evaluated in this order:

| Condition | Priority |
| --- | --- |
| High urgency and at least 10 affected users | critical |
| High urgency or at least 10 affected users | high |
| Medium urgency or at least 3 affected users | medium |
| All other valid combinations | low |

New tickets start with `status="open"` and `assigned_to=None`. IDs use the highest existing numeric ticket ID plus one.

`get_ticket()` normalizes the requested ID and returns a copy. `list_tickets()` also returns copies. `assign_ticket()` updates the stored ticket, requires an exact matching ID and a nonblank staff name, and raises `ValueError` when the ticket is missing.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

Run each module's tests separately:

```bash
python3 -m unittest tests.test_tickets -v
python3 -m unittest tests.test_workflow -v
```

Use the root `tests/` directory for the project's test suite.

## Project structure

| Path | Purpose |
| --- | --- |
| `campusflow/tickets.py` | Ticket validation, creation, IDs, priority, listing, and retrieval |
| `campusflow/workflow.py` | Ticket lookup and staff assignment |
| `tests/test_tickets.py` | Ticket tests |
| `tests/test_workflow.py` | Assignment tests |
| `campusflow/tests/test_workflow.py` | Additional workflow test file |
| `docs/design-decisions.md` | Data model, responsibilities, and design decisions |
| `docs/ai-learning-log.md` | Team learning log |

## Planned work

The team design document identifies these next steps:

- Ticket status changes and reopening
- Priority queue and reports
- Interactive CLI menu
- JSON storage and integration

These items are planned and are not part of the current implementation on `main`.

## Contributing

1. Pull the latest `main`.
2. Create a feature branch.
3. Implement one focused change and add relevant tests.
4. Run the test suite.
5. Commit, push your branch, and open a pull request.

```bash
git switch main
git pull origin main
git switch -c feature/your-change
python3 -m unittest discover -s tests -v
git add path/to/changed-file
git commit -m "Describe your change"
git push -u origin feature/your-change
```

Read [the design decisions](docs/design-decisions.md) before changing business rules.
