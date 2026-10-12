"""Assignment, lifecycle, and open-ticket work queue."""
from .tickets import get_ticket


def _find(tickets, ticket_id):
    normalized = get_ticket(tickets, ticket_id)["id"]
    return next(ticket for ticket in tickets if ticket["id"] == normalized)


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = _find(tickets, ticket_id)
    if ticket["status"] == "resolved":
        raise ValueError("Reopen the resolved ticket before assigning staff.")
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must not be blank.")
    ticket["assigned_to"] = staff_name.strip()
    return ticket.copy()


def change_status(tickets, ticket_id, status):
    ticket = _find(tickets, ticket_id)
    if not isinstance(status, str):
        raise ValueError("Status must be text.")
    status = status.strip().lower()
    transitions = {"open": "in_progress", "in_progress": "resolved"}
    if transitions.get(ticket["status"]) != status:
        raise ValueError("Use open -> in_progress -> resolved; reopen explicitly.")
    if status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign staff before starting work.")
    ticket["status"] = status
    return ticket.copy()


def reopen_ticket(tickets, ticket_id):
    ticket = _find(tickets, ticket_id)
    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")
    ticket["status"] = "open"
    return ticket.copy()


def work_queue(tickets):
    ranks = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return [ticket.copy() for ticket in sorted(
        (ticket for ticket in tickets if ticket["status"] == "open"),
        key=lambda ticket: (ranks[ticket["priority"]], int(ticket["id"][1:])),
    )]
