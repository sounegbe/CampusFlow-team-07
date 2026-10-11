# Design Decisions

- Tickets are stored as a list of dictionaries and passed to each function.
- Invalid input is signalled with ValueError; the CLI catches it and shows the message.
- Status moves: open -> in_progress -> resolved; resolved -> open (reopen) only.
- in_progress -> open is not allowed.
- A ticket must be assigned before it can be in_progress.
- A resolved ticket cannot be assigned until it is reopened.
- The work queue shows only open tickets, sorted by priority then numeric ID.
- Ownership: Engineer A = creation, validation, priority; Engineer B = assign, workflow, queue, reports.