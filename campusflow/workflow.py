def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket_id == ticket["id"]:
            return ticket
    return None
        
def assign_ticket(tickets, ticket_id, staff_name):
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
            raise ValueError("Ticket not found")
    if not staff_name.strip():
            raise ValueError("Staff name cannot be blank")
    ticket["assigned_to"] = staff_name
    return ticket


