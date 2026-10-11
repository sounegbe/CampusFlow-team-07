def validate_ticket_input(title, category, urgency, affected_users):
    """Check ticket details and return cleaned values."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")

    title = title.strip()

    categories = {
        "network": "Network",
        "hardware": "Hardware",
        "software": "Software",
        "other": "Other",
    }

    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    category_key = category.strip().lower()

    if category_key not in categories:
        raise ValueError(
            "Category must be Network, Hardware, Software, or Other."
        )

    category = categories[category_key]

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")

    urgency = urgency.strip().lower()

    if urgency not in ("low", "medium", "high"):
        raise ValueError("Urgency must be low, medium, or high.")

    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer.")

    return title, category, urgency, affected_users

def calculate_priority(urgency, affected_users):
    """Calculate priority from valid, normalized inputs."""

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"

def generate_ticket_id(tickets):
    """Return the next ID based on existing valid ticket IDs."""

    highest_number = 0

    for ticket in tickets:
        ticket_id = ticket["id"]
        number = int(ticket_id[1:])

        if number > highest_number:
            highest_number = number

    return f"T{highest_number + 1:03d}"

def create_ticket(tickets, title, category, urgency, affected_users):
    """Create, store, and return a validated ticket."""

    title, category, urgency, affected_users = validate_ticket_input(
        title, category, urgency, affected_users
    )

    priority = calculate_priority(urgency, affected_users)
    ticket_id = generate_ticket_id(tickets)

    ticket = {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    tickets.append(ticket)

    return ticket

def list_tickets(tickets):
    """Return copies of all tickets without changing the originals."""

    return [ticket.copy() for ticket in tickets]


def get_ticket(tickets, ticket_id):
    """Return a copy of the matching ticket or raise ValueError."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID must not be blank.")

    ticket_id = ticket_id.strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket.copy()

    raise ValueError(f"Ticket '{ticket_id}' was not found.")