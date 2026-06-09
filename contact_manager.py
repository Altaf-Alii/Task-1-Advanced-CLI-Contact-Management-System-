#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║     Advanced CLI Contact Management System (Mini CRM)    ║
║        Task 1 - Full Featured Contact Manager            ║
╚══════════════════════════════════════════════════════════╝
"""

import json
import csv
import os
import re
from datetime import datetime

# ─── File Path for saving contacts ────────────────────────
DATA_FILE = "contacts.json"
PAGE_SIZE = 5   # contacts per page for pagination

# ─── Color Codes for CLI ──────────────────────────────────
class Colors:
    HEADER    = '\033[95m'
    BLUE      = '\033[94m'
    CYAN      = '\033[96m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET     = '\033[0m'

def color(text, code):
    return f"{code}{text}{Colors.RESET}"


# ════════════════════════════════════════════════════════════
#  DATA LAYER — Load / Save
# ════════════════════════════════════════════════════════════

def load_contacts() -> list:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_contacts(contacts: list) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


# ════════════════════════════════════════════════════════════
#  VALIDATION
# ════════════════════════════════════════════════════════════

def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    cleaned = re.sub(r'[\s\-\+\(\)]', '', phone)
    return cleaned.isdigit() and len(cleaned) >= 7


def get_input(prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(color(f"  {prompt}: ", Colors.CYAN)).strip()
        if value or allow_empty:
            return value
        print(color("  ✗ This field cannot be empty. Please try again.", Colors.RED))


# ════════════════════════════════════════════════════════════
#  DISPLAY HELPERS
# ════════════════════════════════════════════════════════════

def print_header():
    print()
    print(color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║    📋  Advanced CLI Contact Management System            ║", Colors.CYAN + Colors.BOLD))
    print(color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN))
    print()


def print_menu():
    print(color("\n  ══════════════ MAIN MENU ══════════════", Colors.YELLOW + Colors.BOLD))
    options = [
        ("1",  "➕  Add New Contact"),
        ("2",  "📋  View All Contacts"),
        ("3",  "🔍  Search Contacts"),
        ("4",  "🔎  Filter Contacts"),
        ("5",  "✏️   Update Contact"),
        ("6",  "🗑️   Delete Contact"),
        ("7",  "💾  Export to CSV"),
        ("8",  "📥  Import from CSV"),
        ("9",  "⭐  Manage Favorites"),
        ("10", "🔤  Sort Contacts"),
        ("0",  "🚪  Exit"),
    ]
    for num, label in options:
        print(f"  {color(num, Colors.GREEN + Colors.BOLD)}. {label}")
    print(color("  ══════════════════════════════════════", Colors.YELLOW))


def print_table(contacts: list, title: str = "Contacts", paginate: bool = True) -> None:
    """Print contacts in a formatted table with optional pagination."""
    if not contacts:
        print(color("\n  ⚠  No contacts to display.", Colors.YELLOW))
        return

    w = {"id": 4, "fav": 4, "name": 20, "phone": 15, "email": 26, "city": 13, "company": 16}

    sep = color(
        f"  +{'─'*w['id']}+{'─'*w['fav']}+{'─'*w['name']}+{'─'*w['phone']}+{'─'*w['email']}+{'─'*w['city']}+{'─'*w['company']}+",
        Colors.BLUE
    )

    def make_header():
        return (
            color("  |", Colors.BLUE) +
            color(f"{'ID':^{w['id']}}", Colors.BOLD) +
            color("|", Colors.BLUE) +
            color(f"{'FAV':^{w['fav']}}", Colors.BOLD) +
            color("|", Colors.BLUE) +
            color(f"{'Full Name':^{w['name']}}", Colors.BOLD) +
            color("|", Colors.BLUE) +
            color(f"{'Phone':^{w['phone']}}", Colors.BOLD) +
            color("|", Colors.BLUE) +
            color(f"{'Email':^{w['email']}}", Colors.BOLD) +
            color("|", Colors.BLUE) +
            color(f"{'City':^{w['city']}}", Colors.BOLD) +
            color("|", Colors.BLUE) +
            color(f"{'Company':^{w['company']}}", Colors.BOLD) +
            color("|", Colors.BLUE)
        )

    total   = len(contacts)
    pages   = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page    = 1

    while True:
        start = (page - 1) * PAGE_SIZE
        end   = start + PAGE_SIZE
        chunk = contacts[start:end] if paginate else contacts

        print(color(f"\n  {'═'*6} {title} ({total} total | Page {page}/{pages}) {'═'*6}", Colors.CYAN + Colors.BOLD))
        print(sep)
        print(make_header())
        print(sep)

        for c in chunk:
            star = color("★", Colors.YELLOW) if c.get("favorite") else " "
            row = (
                color("  |", Colors.BLUE) +
                f"{str(c['id']):^{w['id']}}" +
                color("|", Colors.BLUE) +
                f"{star:^{w['fav']}}" +
                color("|", Colors.BLUE) +
                f"{c['name'][:w['name']-1]:<{w['name']}}" +
                color("|", Colors.BLUE) +
                f"{c['phone'][:w['phone']-1]:<{w['phone']}}" +
                color("|", Colors.BLUE) +
                f"{c['email'][:w['email']-1]:<{w['email']}}" +
                color("|", Colors.BLUE) +
                f"{c['city'][:w['city']-1]:<{w['city']}}" +
                color("|", Colors.BLUE) +
                f"{c['company'][:w['company']-1]:<{w['company']}}" +
                color("|", Colors.BLUE)
            )
            print(row)

        print(sep)

        # If no pagination needed or only 1 page, stop
        if not paginate or pages == 1:
            break

        # Pagination controls
        print(color(f"\n  Page {page}/{pages}  |  ", Colors.YELLOW) +
              color("[N]", Colors.GREEN) + " Next  " +
              color("[P]", Colors.GREEN) + " Prev  " +
              color("[Q]", Colors.RED)   + " Quit")
        nav = input(color("  Navigate: ", Colors.CYAN)).strip().lower()

        if nav == 'n' and page < pages:
            page += 1
        elif nav == 'p' and page > 1:
            page -= 1
        elif nav == 'q':
            break
        else:
            print(color("  ⚠  Invalid option or already at boundary.", Colors.YELLOW))


def generate_id(contacts: list) -> int:
    return max((c["id"] for c in contacts), default=0) + 1


# ════════════════════════════════════════════════════════════
#  CORE FEATURES
# ════════════════════════════════════════════════════════════

# ── 1. Add Contact ──────────────────────────────────────────
def add_contact():
    print(color("\n  ══ ➕ Add New Contact ══", Colors.GREEN + Colors.BOLD))

    name = get_input("Full Name")

    while True:
        phone = get_input("Phone Number")
        if validate_phone(phone):
            break
        print(color("  ✗ Invalid phone number. Use digits, spaces, dashes or + sign.", Colors.RED))

    while True:
        email = get_input("Email Address")
        if validate_email(email):
            break
        print(color("  ✗ Invalid email format. Example: user@example.com", Colors.RED))

    city    = get_input("City")
    company = get_input("Company")

    contacts = load_contacts()

    if any(c["email"].lower() == email.lower() for c in contacts):
        print(color(f"\n  ✗ A contact with email '{email}' already exists!", Colors.RED))
        return

    contact = {
        "id":       generate_id(contacts),
        "name":     name,
        "phone":    phone,
        "email":    email,
        "city":     city,
        "company":  company,
        "favorite": False,
        "created":  datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    contacts.append(contact)
    save_contacts(contacts)
    print(color(f"\n  ✓ Contact '{name}' added successfully! (ID: {contact['id']})", Colors.GREEN))


# ── 2. View All Contacts ─────────────────────────────────────
def view_contacts():
    contacts = load_contacts()
    print_table(contacts, "All Contacts", paginate=True)


# ── 3. Search Contacts ───────────────────────────────────────
def search_contacts():
    print(color("\n  ══ 🔍 Search Contacts ══", Colors.BLUE + Colors.BOLD))
    print("  Search by:")
    print(f"  {color('1', Colors.GREEN)}. Name  {color('2', Colors.GREEN)}. Phone  {color('3', Colors.GREEN)}. Email")

    choice    = input(color("  Choose (1/2/3): ", Colors.CYAN)).strip()
    field_map = {"1": "name", "2": "phone", "3": "email"}

    if choice not in field_map:
        print(color("  ✗ Invalid option.", Colors.RED))
        return

    field   = field_map[choice]
    query   = get_input(f"Enter {field} to search (partial match)")
    contacts = load_contacts()
    results  = [c for c in contacts if query.lower() in c[field].lower()]
    print_table(results, f"Search Results for '{query}'", paginate=True)


# ── 4. Filter Contacts ───────────────────────────────────────
def filter_contacts():
    print(color("\n  ══ 🔎 Filter Contacts ══", Colors.BLUE + Colors.BOLD))
    print("  Filter by:")
    print(f"  {color('1', Colors.GREEN)}. City  {color('2', Colors.GREEN)}. Company")

    choice    = input(color("  Choose (1/2): ", Colors.CYAN)).strip()
    field_map = {"1": "city", "2": "company"}

    if choice not in field_map:
        print(color("  ✗ Invalid option.", Colors.RED))
        return

    field    = field_map[choice]
    query    = get_input(f"Enter {field} to filter")
    contacts = load_contacts()
    results  = [c for c in contacts if query.lower() in c[field].lower()]
    print_table(results, f"Filtered by {field.capitalize()} = '{query}'", paginate=True)


# ── 5. Update Contact ────────────────────────────────────────
def update_contact():
    print(color("\n  ══ ✏️  Update Contact ══", Colors.YELLOW + Colors.BOLD))
    contacts = load_contacts()

    if not contacts:
        print(color("  ⚠  No contacts available.", Colors.YELLOW))
        return

    view_contacts()

    try:
        cid = int(input(color("\n  Enter Contact ID to update: ", Colors.CYAN)).strip())
    except ValueError:
        print(color("  ✗ Invalid ID.", Colors.RED))
        return

    idx = next((i for i, c in enumerate(contacts) if c["id"] == cid), None)
    if idx is None:
        print(color(f"  ✗ Contact with ID {cid} not found.", Colors.RED))
        return

    c = contacts[idx]
    print(color(f"\n  Editing: {c['name']} (leave blank to keep current value)", Colors.CYAN))

    fields = ["name", "phone", "email", "city", "company"]
    for field in fields:
        new_val = input(color(f"  {field.capitalize()} [{c[field]}]: ", Colors.CYAN)).strip()
        if new_val:
            if field == "phone" and not validate_phone(new_val):
                print(color(f"  ✗ Invalid phone, keeping old value.", Colors.RED))
                continue
            if field == "email" and not validate_email(new_val):
                print(color(f"  ✗ Invalid email, keeping old value.", Colors.RED))
                continue
            c[field] = new_val

    c["updated"]  = datetime.now().strftime("%Y-%m-%d %H:%M")
    contacts[idx] = c
    save_contacts(contacts)
    print(color(f"\n  ✓ Contact ID {cid} updated successfully!", Colors.GREEN))


# ── 6. Delete Contact ────────────────────────────────────────
def delete_contact():
    print(color("\n  ══ 🗑️  Delete Contact ══", Colors.RED + Colors.BOLD))
    contacts = load_contacts()

    if not contacts:
        print(color("  ⚠  No contacts available.", Colors.YELLOW))
        return

    view_contacts()

    try:
        cid = int(input(color("\n  Enter Contact ID to delete: ", Colors.CYAN)).strip())
    except ValueError:
        print(color("  ✗ Invalid ID.", Colors.RED))
        return

    contact = next((c for c in contacts if c["id"] == cid), None)
    if not contact:
        print(color(f"  ✗ Contact with ID {cid} not found.", Colors.RED))
        return

    confirm = input(color(f"  ⚠  Delete '{contact['name']}'? (yes/no): ", Colors.YELLOW)).strip().lower()
    if confirm in ("yes", "y"):
        contacts = [c for c in contacts if c["id"] != cid]
        save_contacts(contacts)
        print(color(f"\n  ✓ Contact '{contact['name']}' deleted.", Colors.GREEN))
    else:
        print(color("  ✗ Deletion cancelled.", Colors.YELLOW))


# ── 7. Export to CSV ─────────────────────────────────────────
def export_csv():
    contacts = load_contacts()
    if not contacts:
        print(color("  ⚠  No contacts to export.", Colors.YELLOW))
        return

    filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fields   = ["id", "name", "phone", "email", "city", "company", "favorite", "created"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(contacts)

    print(color(f"\n  ✓ {len(contacts)} contacts exported to '{filename}'", Colors.GREEN))


# ── 8. Import from CSV ───────────────────────────────────────
def import_csv():
    print(color("\n  ══ 📥 Import from CSV ══", Colors.BLUE + Colors.BOLD))
    filename = input(color("  Enter CSV filename: ", Colors.CYAN)).strip()

    if not os.path.exists(filename):
        print(color(f"  ✗ File '{filename}' not found.", Colors.RED))
        return

    contacts        = load_contacts()
    existing_emails = {c["email"].lower() for c in contacts}
    imported        = 0
    skipped         = 0

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "").strip()
            if not email or email.lower() in existing_emails:
                skipped += 1
                continue

            contact = {
                "id":       generate_id(contacts),
                "name":     row.get("name", "Unknown").strip(),
                "phone":    row.get("phone", "").strip(),
                "email":    email,
                "city":     row.get("city", "").strip(),
                "company":  row.get("company", "").strip(),
                "favorite": False,
                "created":  datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            contacts.append(contact)
            existing_emails.add(email.lower())
            imported += 1

    save_contacts(contacts)
    print(color(f"\n  ✓ Import complete: {imported} added, {skipped} skipped.", Colors.GREEN))


# ════════════════════════════════════════════════════════════
#  BONUS FEATURE 1 — ⭐ Favorites
# ════════════════════════════════════════════════════════════

def manage_favorites():
    print(color("\n  ══ ⭐ Manage Favorites ══", Colors.YELLOW + Colors.BOLD))
    print(f"  {color('1', Colors.GREEN)}. Star / Unstar a contact")
    print(f"  {color('2', Colors.GREEN)}. View all starred contacts")

    choice = input(color("  Choose (1/2): ", Colors.CYAN)).strip()

    contacts = load_contacts()
    if not contacts:
        print(color("  ⚠  No contacts available.", Colors.YELLOW))
        return

    if choice == "1":
        print_table(contacts, "All Contacts", paginate=False)
        try:
            cid = int(input(color("\n  Enter Contact ID to toggle star: ", Colors.CYAN)).strip())
        except ValueError:
            print(color("  ✗ Invalid ID.", Colors.RED))
            return

        idx = next((i for i, c in enumerate(contacts) if c["id"] == cid), None)
        if idx is None:
            print(color(f"  ✗ Contact with ID {cid} not found.", Colors.RED))
            return

        contacts[idx]["favorite"] = not contacts[idx].get("favorite", False)
        status = "★ Starred" if contacts[idx]["favorite"] else "☆ Unstarred"
        save_contacts(contacts)
        print(color(f"\n  ✓ '{contacts[idx]['name']}' is now {status}!", Colors.GREEN))

    elif choice == "2":
        favorites = [c for c in contacts if c.get("favorite")]
        print_table(favorites, "⭐ Starred Contacts", paginate=True)

    else:
        print(color("  ✗ Invalid option.", Colors.RED))


# ════════════════════════════════════════════════════════════
#  BONUS FEATURE 2 — 🔤 Sort Contacts
# ════════════════════════════════════════════════════════════

def sort_contacts():
    print(color("\n  ══ 🔤 Sort Contacts ══", Colors.BLUE + Colors.BOLD))
    print("  Sort by:")
    print(f"  {color('1', Colors.GREEN)}. Name (A → Z)")
    print(f"  {color('2', Colors.GREEN)}. Name (Z → A)")
    print(f"  {color('3', Colors.GREEN)}. Recently Added")
    print(f"  {color('4', Colors.GREEN)}. Oldest First")
    print(f"  {color('5', Colors.GREEN)}. City (A → Z)")
    print(f"  {color('6', Colors.GREEN)}. Company (A → Z)")
    print(f"  {color('7', Colors.GREEN)}. Starred First")

    choice = input(color("  Choose (1-7): ", Colors.CYAN)).strip()

    contacts = load_contacts()
    if not contacts:
        print(color("  ⚠  No contacts available.", Colors.YELLOW))
        return

    sort_map = {
        "1": ("Name A→Z",        lambda c: c["name"].lower(),                        False),
        "2": ("Name Z→A",        lambda c: c["name"].lower(),                        True),
        "3": ("Recently Added",  lambda c: c.get("created", ""),                     True),
        "4": ("Oldest First",    lambda c: c.get("created", ""),                     False),
        "5": ("City A→Z",        lambda c: c["city"].lower(),                        False),
        "6": ("Company A→Z",     lambda c: c["company"].lower(),                     False),
        "7": ("Starred First",   lambda c: (not c.get("favorite", False), c["name"].lower()), False),
    }

    if choice not in sort_map:
        print(color("  ✗ Invalid option.", Colors.RED))
        return

    label, key_fn, reverse = sort_map[choice]
    sorted_contacts = sorted(contacts, key=key_fn, reverse=reverse)
    print_table(sorted_contacts, f"Sorted by: {label}", paginate=True)


# ════════════════════════════════════════════════════════════
#  MAIN LOOP
# ════════════════════════════════════════════════════════════

def main():
    print_header()

    menu_actions = {
        "1":  add_contact,
        "2":  view_contacts,
        "3":  search_contacts,
        "4":  filter_contacts,
        "5":  update_contact,
        "6":  delete_contact,
        "7":  export_csv,
        "8":  import_csv,
        "9":  manage_favorites,
        "10": sort_contacts,
    }

    while True:
        print_menu()
        choice = input(color("\n  Enter your choice: ", Colors.BOLD + Colors.GREEN)).strip()

        if choice == "0":
            print(color("\n  👋 Goodbye! Your contacts have been saved.\n", Colors.CYAN))
            break
        elif choice in menu_actions:
            menu_actions[choice]()
        else:
            print(color("  ✗ Invalid option. Please choose from the menu.", Colors.RED))

        input(color("\n  Press Enter to continue...", Colors.YELLOW))


if __name__ == "__main__":
    main()
