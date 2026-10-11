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