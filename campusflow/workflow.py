"""Ticket assignment, lifecycle, queue, and reporting."""

from .tickets import get_ticket
from .reports import ticket_report

ALLOWED_MOVES = {
    "open": "in_progress",
    "in_progress": "resolved",
    "resolved": "open",
}
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def find_ticket(tickets, ticket_id):
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID must not be blank.")
    normalized = ticket_id.strip().upper()
    return next(
        (ticket for ticket in tickets if ticket["id"] == normalized),
        None,
    )


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


def change_status(tickets, ticket_id, new_status):
    ticket = _find(tickets, ticket_id)
    if not isinstance(new_status, str):
        raise ValueError("Status must be text.")
    new_status = new_status.strip().lower()
    if ALLOWED_MOVES.get(ticket["status"]) != new_status:
        raise ValueError(
            f"Cannot move from {ticket['status']} to {new_status}"
        )
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign staff before starting work.")
    ticket["status"] = new_status
    return ticket.copy()


def reopen_ticket(tickets, ticket_id):
    ticket = _find(tickets, ticket_id)
    if ticket["status"] != "resolved":
        raise ValueError("Only resolved tickets can be reopened.")
    return change_status(tickets, ticket_id, "open")


def get_work_queue(tickets):
    return [
        ticket.copy()
        for ticket in sorted(
            (ticket for ticket in tickets if ticket["status"] == "open"),
            key=lambda ticket: (
                PRIORITY_ORDER[ticket["priority"]],
                int(ticket["id"][1:]),
            ),
        )
    ]


def work_queue(tickets):
    return get_work_queue(tickets)


def build_report(tickets):
    return ticket_report(tickets)
