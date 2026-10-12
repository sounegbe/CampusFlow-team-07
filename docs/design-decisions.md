
# Design Decisions

- Tickets are stored as a list of dictionaries and passed to each function.
- Invalid input is signalled with ValueError; the CLI catches it and shows the message.
- Status moves: open -> in_progress -> resolved; resolved -> open (reopen) only.
- in_progress -> open is not allowed.
- A ticket must be assigned before it can be in_progress.
- A resolved ticket cannot be assigned until it is reopened.
- The work queue shows only open tickets, sorted by priority then numeric ID.
- Ownership: Engineer A = creation, validation, priority; Engineer B = assign, workflow, queue, reports.

# CampusFlow Design Decisions

## Responsibilities
- Engineer A: ticket creation, validation, priority, unique IDs,
  listing and viewing tickets, and matching tests.
- Engineer B: assignment, status changes, reopening, queue,
  reports, and matching tests.
- Both: CLI menu, JSON storage, integration, and documentation.

## Ticket storage
Tickets are stored in a list of dictionaries.
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
- Invalid input raises ValueError.
- Failed operations must not change the ticket list.

## Function boundaries
- Business functions receive arguments and return results.
- input() and display messages belong in main.py.
- Storage functions belong in storage.py.

