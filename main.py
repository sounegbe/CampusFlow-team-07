"""CampusFlow terminal menu. Run: python3 main.py."""
import argparse
import json
from pathlib import Path

from campusflow.tickets import create_ticket, get_ticket, list_tickets
from campusflow.workflow import assign_ticket, change_status, reopen_ticket, work_queue
from campusflow.reports import ticket_report
from campusflow.storage import load_tickets, save_tickets

DEFAULT_DATA = Path(__file__).resolve().parent / "data" / "tickets.json"
MENU = "\n1 Create | 2 List | 3 View | 4 Assign | 5 Change status | 6 Reopen | 7 Queue | 8 Report | 0 Exit"


def display(value):
    print(json.dumps(value, indent=2, ensure_ascii=False))


def run(path):
    try:
        tickets = load_tickets(path)
    except (ValueError, OSError) as error:
        print(f"Startup error: {error}. Existing data was not changed.")
        return 1
    print("CampusFlow - Campus support helpdesk")
    while True:
        try:
            print(MENU)
            choice = input("Choose: ").strip()
            if choice == "0":
                print("Goodbye. Successful changes are already saved.")
                return 0
            if choice == "2":
                display(list_tickets(tickets))
            elif choice == "3":
                display(get_ticket(tickets, input("Ticket ID: ")))
            elif choice == "7":
                display(work_queue(tickets))
            elif choice == "8":
                display(ticket_report(tickets))
            elif choice in ("1", "4", "5", "6"):
                candidate = [ticket.copy() for ticket in tickets]
                if choice == "1":
                    title = input("Title: ")
                    category = input("Category (Network/Hardware/Software/Other): ")
                    urgency = input("Urgency (low/medium/high): ")
                    raw_count = input("Affected users (positive integer): ").strip()
                    if not raw_count.isascii() or not raw_count.isdigit():
                        raise ValueError("Affected users must be a positive integer.")
                    result = create_ticket(candidate, title, category, urgency, int(raw_count))
                elif choice == "4":
                    result = assign_ticket(candidate, input("Ticket ID: "), input("Staff name: "))
                elif choice == "5":
                    result = change_status(candidate, input("Ticket ID: "), input("New status (in_progress/resolved): "))
                else:
                    result = reopen_ticket(candidate, input("Ticket ID to reopen: "))
                save_tickets(candidate, path)
                tickets = candidate
                display(result)
            else:
                print("Choose a menu option from 0 to 8.")
        except (ValueError, OSError) as error:
            print(f"Error: {error}. No changes were committed.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye. Successful changes are already saved.")
            return 0


def main():
    parser = argparse.ArgumentParser(description="CampusFlow helpdesk")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    return run(parser.parse_args().data)


if __name__ == "__main__":
    raise SystemExit(main())
