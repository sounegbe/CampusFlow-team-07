# CampusFlow

Python terminal helpdesk for campus technical support. Create and prioritize support tickets, assign staff, track progress, and save records between sessions. Uses Python 3.10+ and the standard library; no third-party packages are required.

## Setup

```bash
git clone https://github.com/sounegbe/CampusFlow-team-07.git
cd CampusFlow-team-07
python3 --version
```

If you already have the repository, ensure your working tree is clean before switching to `main` and running `git pull --ff-only origin main`.

## Run

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

Optional isolated data file:

```bash
python3 main.py --data /tmp/campusflow-demo.json
```

Run commands from the repository root. On Windows, use `py` instead of `python3` if needed.

| Option | Action |
| --- | --- |
| 1 | Create a ticket |
| 2 | List all tickets |
| 3 | View a ticket by ID |
| 4 | Assign staff |
| 5 | Change status |
| 6 | Reopen a resolved ticket |
| 7 | View the open-ticket queue |
| 8 | View totals by status and priority |
| 0 | Exit |

Titles and staff names must be nonblank. Categories are Network, Hardware, Software, or Other; urgency is low, medium, or high. Category, urgency, status, and lookup ID case is normalized. Affected users must be a positive integer. New tickets begin with status `open`, no assignee, and sequential IDs starting at `T001`.

## Rules

Priority uses the first matching rule:

| Condition | Priority |
| --- | --- |
| High urgency AND at least 10 users | critical |
| High urgency OR at least 10 users | high |
| Medium urgency OR at least 3 users | medium |
| All other valid combinations | low |

Assign staff before moving from `open` to `in_progress`, then to `resolved`. Skipping directly from `open` to `resolved`, or moving from `in_progress` back to `open`, is rejected. Reopen resolved tickets using menu option 6. The Python API also supports `change_status(tickets, ticket_id, "open")` for resolved tickets. Reopening retains staff; resolved tickets cannot be reassigned until reopened.

The queue includes open tickets only, ordered critical/high/medium/low, then numeric ID. Reports include zero counts.

## Storage

Default file: data/tickets.json beside main.py. Every successful mutation is saved using a temporary file and atomic replacement before it becomes the CLI's current state. Missing data starts empty. Malformed JSON or invalid records stop startup without overwriting data. Loaded records are checked for valid fields, normalized inputs, priority consistency, assignment/status consistency, and unique canonical IDs.

To start fresh, exit and move your data file to a backup location. Do not delete real support data accidentally. No automatic reset occurs on corruption.

## Tests

The current root test suite contains **60 passing tests**, covering ticket validation and creation, priority boundaries, malformed IDs, viewing copies, assignment and status transitions, both reopening methods, queue ordering, reports, JSON round trips, IDs after reload, corrupt data, failed atomic replacement, and end-to-end CLI subprocess runs.

```bash
python3 -m unittest discover -s tests -v
```

Use the root `tests/` directory for the complete suite. Tests use temporary files for storage and CLI checks.

## Project structure

| Path | Purpose |
| --- | --- |
| `main.py` | Interactive CLI and save-before-publish mutations |
| `campusflow/tickets.py` | Validation, creation, priority, IDs, listing, and lookup |
| `campusflow/workflow.py` | Assignment, lifecycle, reopening, queue, and report compatibility functions |
| `campusflow/reports.py` | Ticket totals by status and priority |
| `campusflow/storage.py` | Validated JSON loading and atomic saves |
| `tests/` | Ticket, workflow, storage, and CLI tests |
| `docs/design-decisions.md` | Business rules and integration contracts |
| `docs/ai-learning-log.md` | Team AI learning log |

## Contributions and assessment evidence

- Engineer A: 2solo / sounegbe. Ticket functions and original 36 tests developed with AI guidance.
- Engineer B: Symplythatguy (Daniel Okoh). Wrote `find_ticket` and `assign_ticket` and their first tests with step-by-step AI mentoring. Created Issues #2 and #3, opened PR #6, resolved the merge conflict in `docs/design-decisions.md`, merged the shared design decisions, and ran the full suite (60 tests) and the CLI on `main`. Repository setup commit and AI learning log are his.
- AI-supplied code: at Engineer B's request, because of the deadline, an AI assistant supplied `change_status`, `get_work_queue`, `build_report` and their tests. Storage, CLI, and the 12 integration tests were also AI-supplied under sounegbe's authorization. These parts must not be represented as independently authored work.
- Review evidence: Engineer B's review of Engineer A's work is recorded in the PR comments, and only counts once those comments are posted.

PRs:

- [Repository setup #1](https://github.com/sounegbe/CampusFlow-team-07/pull/1)
- [Engineer A, Part A #4](https://github.com/sounegbe/CampusFlow-team-07/pull/4)
- [Engineer B, workflow, queue, and reports #6](https://github.com/sounegbe/CampusFlow-team-07/pull/6)
- [Engineer B, README and AI log #8](https://github.com/sounegbe/CampusFlow-team-07/pull/8) (merged before partner review; review requested afterwards)
- [All pull requests](https://github.com/sounegbe/CampusFlow-team-07/pulls?q=is%3Apr)

PR #4 was already merged when completion began; its reviews endpoint returned no submitted reviews. Genuine cross-review, each fellow's real code/test contributions, personal learning logs, and technical defence remain required by the sprint. AI completion does not satisfy those human requirements automatically.

## Limitations

Single-process local CLI; no locking for concurrent writers, authentication, website, database, or ticket deletion. Viewing copies are shallow, suitable for the current scalar-only ticket schema. Core priority calculation expects validated inputs. Storage validation is stricter than creation helpers about canonical existing IDs.

## Demonstration

Use a separate data file to keep demo records separate from existing tickets:

```bash
python3 main.py --data data/demo-tickets.json
```

1. Create a Network ticket with high urgency and 12 affected users; verify critical priority.
2. Try creating a ticket with zero affected users; verify rejection.
3. Try moving the unassigned ticket to `in_progress`; verify rejection.
4. Assign staff, move to `in_progress`, then to `resolved`.
5. Try assigning the resolved ticket; verify rejection, then reopen with option 6.
6. Check the queue and report using options 7 and 8.
7. Exit with option 0, restart with the same data path, and verify the ticket remains.
8. Create another ticket and verify its ID increments.

For assessment, run the full test suite and present actual partner review evidence alongside the demo.
