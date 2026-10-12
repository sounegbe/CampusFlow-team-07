# CampusFlow

Python terminal helpdesk for campus technical support. Standard library only; Python 3.10+ (verified with Python 3.12.14 in the completion environment).

## Run

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

Optional isolated data file:

```bash
python3 main.py --data /tmp/campusflow-demo.json
```

Menu: create, list, view, assign, change status, explicitly reopen, open-ticket queue, reports, and exit. Enter category Network/Hardware/Software/Other, urgency low/medium/high, and a positive integer user count. Text case is normalized.

## Rules

Priority uses the first matching rule: high urgency AND >=10 users is critical; high urgency OR >=10 users is high; medium urgency OR >=3 users is medium; otherwise low.

Assign nonblank staff before open -> in_progress -> resolved. Resolved tickets cannot be assigned or progressed until explicitly reopened to open. Reopening retains staff. The queue includes open tickets only, ordered critical/high/medium/low, then numeric ID. Reports include zero counts.

## Storage

Default file: data/tickets.json beside main.py. Every successful mutation is saved using a temporary file and atomic replacement before it becomes the CLI's current state. Missing data starts empty. Malformed JSON or invalid records stop startup without overwriting data. Loaded records are checked for valid fields, normalized inputs, priority consistency, assignment/status consistency, and unique canonical IDs.

To start fresh, exit and move your data file to a backup location. Do not delete real support data accidentally. No automatic reset occurs on corruption.

## Tests

48 tests passed during completion: ticket inputs and creation, priorities and boundaries, malformed IDs, viewing copies, assignment/lifecycle/reopening, queue ordering, reports, JSON round trip, new IDs after reload, corrupt data, failed atomic replacement, and end-to-end CLI subprocess runs.

## Contributions and assessment evidence

- Engineer A: 2solo / sounegbe. Ticket functions and original 36 tests developed with AI guidance.
- Engineer B: Symplythatguy (Daniel Okoh). Wrote `find_ticket` and `assign_ticket` and their first tests with step-by-step AI mentoring. Created Issues #2 and #3, opened PR #6, resolved the merge conflict in `docs/design-decisions.md`, merged the shared design decisions, and ran the full suite (60 tests) and the CLI on `main`. Repository setup commit and AI learning log are his.
- AI-supplied code: at Engineer B's request, because of the deadline, an AI assistant supplied `change_status`, `get_work_queue`, `build_report` and their tests. Storage, CLI, and the 12 integration tests were also AI-supplied under sounegbe's authorization. These parts must not be represented as independently authored work.
- Review evidence: Engineer B's review of Engineer A's work is recorded in the PR comments, and only counts once those comments are posted.

PRs: [setup #1](https://github.com/sounegbe/CampusFlow-team-07/pull/1), [Part A #4](https://github.com/sounegbe/CampusFlow-team-07/pull/4), [all PRs](https://github.com/sounegbe/CampusFlow-team-07/pulls?q=is%3Apr).

PR #4 was already merged when completion began; its reviews endpoint returned no submitted reviews. Genuine cross-review, each fellow's real code/test contributions, personal learning logs, and technical defence remain required by the sprint. AI completion does not satisfy those human requirements automatically.

## Limitations

Single-process local CLI; no locking for concurrent writers, authentication, website, database, or ticket deletion. Viewing copies are shallow, suitable for the current scalar-only ticket schema. Core priority calculation expects validated inputs. Storage validation is stricter than creation helpers about canonical existing IDs.

## Demonstration

Create a high/12 ticket; reject zero users; try starting an unassigned ticket; assign staff; progress and resolve; reject reassignment until reopening; inspect queue/report; exit and restart; create another ticket to verify the next ID; run all tests and show actual partner reviews.
