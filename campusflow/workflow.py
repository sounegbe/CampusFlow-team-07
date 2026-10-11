ALLOWED_MOVES = {
    "open": "in_progress",
    "in_progress": "resolved",
    "resolved": "open",
}

PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket_id == ticket["id"]:
            return ticket
    return None


def assign_ticket(tickets, ticket_id, staff_name):
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError("Ticket not found")
    if ticket.get("status") == "resolved":
        raise ValueError("Reopen the ticket before changing it")
    if not staff_name.strip():
        raise ValueError("Staff name cannot be blank")
    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError("Ticket not found")
    if ALLOWED_MOVES.get(ticket["status"]) != new_status:
        raise ValueError(f"Cannot move from {ticket['status']} to {new_status}")
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Cannot start an unassigned ticket")
    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    open_tickets = [t for t in tickets if t["status"] == "open"]
    return sorted(
        open_tickets,
        key=lambda t: (PRIORITY_ORDER[t["priority"]], int(t["id"][1:])),
    )


def build_report(tickets):
    by_status = {status: 0 for status in ALLOWED_MOVES}
    by_priority = {priority: 0 for priority in PRIORITY_ORDER}
    for ticket in tickets:
        by_status[ticket["status"]] += 1
        by_priority[ticket["priority"]] += 1
    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }