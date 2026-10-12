# CampusFlow Design Decisions

## Responsibilities
- Engineer A: ticket creation, validation, priority, unique IDs,
  listing and viewing tickets, and matching tests.
- Engineer B: assignment, status changes, reopening, queue,
  reports, and matching tests.
- Both: CLI menu, JSON storage, integration, and documentation.

## Ticket storage
Tickets are stored in a list of dictionaries and passed to each function.
Each ticket contains:
id, title, category, urgency, affected_users, priority,
status, assigned_to.

## New tickets
- Initial status: open
- Initial assigned_to: None
- IDs start at T001.
- New IDs use the highest existing numeric ID plus one.

## Input rules
- Title must not be blank.
- Categories: Network, Hardware, Software, Other.
- Urgency: low, medium, high.
- Accept valid case variations and normalize them.
- affected_users must be a positive integer.
- Invalid input raises ValueError; the CLI catches it and shows the message.
- Failed operations must not change the ticket list.

## Workflow rules
- Status moves: open -> in_progress -> resolved; resolved -> open (reopen) only.
- in_progress -> open is not allowed.
- A ticket must be assigned before it can be in_progress.
- A resolved ticket cannot be assigned until it is reopened.
- The work queue shows only open tickets, sorted by priority then numeric ID.

## Function boundaries
- Business functions receive arguments and return results.
- input() and display messages belong in main.py.
- Storage functions belong in storage.py.

## Completion integration contracts
- assign_ticket(tickets, ticket_id, staff_name), change_status(tickets, ticket_id, status), and reopen_ticket(tickets, ticket_id) mutate the original collection only after validation and return copies.
- work_queue(tickets) returns copies of open tickets sorted by priority and numeric ID.
- ticket_report(tickets) returns total, by_status, and by_priority with zero counts included.
- load_tickets(path) validates records and raises on corrupt data; missing files return an empty list.
- save_tickets(tickets, path) validates first and atomically replaces the JSON file.
- CLI mutations use a candidate copy and publish it to memory only after saving succeeds.
- Queue means status open, excluding in_progress and resolved. Explicit reopening retains the existing assignee.
- Completion modules and tests were AI-authored with user authorization. Human partner review and genuine individual contributions remain assessment tasks.
