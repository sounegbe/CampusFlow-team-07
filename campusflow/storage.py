"""Validated JSON persistence with atomic replacement."""
import json
import os
import tempfile
from pathlib import Path

from .tickets import calculate_priority, generate_ticket_id, validate_ticket_input

FIELDS = {"id", "title", "category", "urgency", "affected_users", "priority", "status", "assigned_to"}


def validate_stored_tickets(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Stored tickets must be a JSON list.")
    seen = set()
    for ticket in tickets:
        if not isinstance(ticket, dict) or set(ticket) != FIELDS:
            raise ValueError("Each stored ticket must contain exactly the eight ticket fields.")
        generate_ticket_id([ticket])
        number = int(ticket["id"][1:])
        if ticket["id"] != f"T{number:03d}" or number in seen:
            raise ValueError("Ticket IDs must be canonical and unique.")
        seen.add(number)
        cleaned = validate_ticket_input(ticket["title"], ticket["category"], ticket["urgency"], ticket["affected_users"])
        if cleaned != (ticket["title"], ticket["category"], ticket["urgency"], ticket["affected_users"]):
            raise ValueError("Stored ticket inputs must be normalized.")
        if ticket["priority"] != calculate_priority(ticket["urgency"], ticket["affected_users"]):
            raise ValueError("Stored priority does not match the ticket inputs.")
        if ticket["status"] not in ("open", "in_progress", "resolved"):
            raise ValueError("Invalid stored ticket status.")
        staff = ticket["assigned_to"]
        if staff is not None and (not isinstance(staff, str) or not staff.strip() or staff != staff.strip()):
            raise ValueError("Invalid stored staff name.")
        if ticket["status"] != "open" and staff is None:
            raise ValueError("Active or resolved tickets must have assigned staff.")
    return tickets


def load_tickets(path):
    path = Path(path)
    try:
        with path.open(encoding="utf-8") as stream:
            tickets = json.load(stream)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError(f"Cannot read ticket data from {path}: {error}") from error
    return validate_stored_tickets(tickets)


def save_tickets(tickets, path):
    validate_stored_tickets(tickets)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
            temporary = stream.name
            json.dump(tickets, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
