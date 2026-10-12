"""Ticket totals, including zero-count categories."""


def ticket_report(tickets):
    statuses = dict.fromkeys(("open", "in_progress", "resolved"), 0)
    priorities = dict.fromkeys(("critical", "high", "medium", "low"), 0)
    for ticket in tickets:
        statuses[ticket["status"]] += 1
        priorities[ticket["priority"]] += 1
    return {"total": len(tickets), "by_status": statuses, "by_priority": priorities}
