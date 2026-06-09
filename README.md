<img width="960" height="540" alt="image" src="https://github.com/user-attachments/assets/9cbf8224-ae9f-4a90-979d-7c03841bb355" /> Advanced CLI Contact Management System

> A professional **Command-Line Contact Management System** built with Python — simulating a real-world mini CRM (Customer Relationship Management) tool.


 Features

 Core Features
| Feature | Description |
|--------|-------------|
| ➕ Add Contact | Add new contacts with full validation |
| 📋 View Contacts | Display all contacts in a formatted table |
| 🔍 Search Contacts | Search by Name, Phone, or Email (partial match) |
| 🔎 Filter Contacts | Filter by City or Company |
| ✏️ Update Contact | Edit any field of an existing contact |
| 🗑️ Delete Contact | Delete contact with confirmation prompt |
| 💾 Export to CSV | Export all contacts to a CSV file |
| 📥 Import from CSV | Import contacts from a CSV file |

 Bonus Features
| Feature | Description |
|--------|-------------|
| ⭐ Favorites | Star/unstar contacts and view starred list |
| 🔤 Sort Contacts | Sort by Name, Date Added, City, Company, or Starred |
| 📄 Pagination | Browse large contact lists page by page |


 Requirements

- Python 3.x
- No external libraries needed — uses built-in modules only

---

 How to Run

**1. Clone the repository:**
git clone https://github.com/Altaf-Alii/Task-1-Advanced-CLI-Contact-Management-System-

**2. Go to project folder:**
```bash
cd Task-1-Advanced-CLI-Contact-Management-System
```

**3. Run the program:**
```bash
python contact_manager.py
```

> On some systems use `python3` or `py` instead of `python`

---

 Project Structure

```
Contact-Management-System/
│
├── contact_manager.py      Main program file
├── contacts.json           Auto-generated data file (created on first run)
└── README.md               Project documentation
```

---

 Contact Fields

Each contact stores the following information:

- 🆔 Unique ID (auto-generated)
- 👤 Full Name
- 📞 Phone Number
- 📧 Email Address
- 🏙️ City
- 🏢 Company
- ⭐ Favorite (starred or not)
- 🕐 Date Created

---
 How to Use

 Add a Contact
```
Enter your choice: 1
Full Name: Ali Hassan
Phone Number: 03001234567
Email Address: ali@gmail.com
City: Karachi
Company: TechCorp
✓ Contact 'Ali Hassan' added successfully! (ID: 1)
```

 Search a Contact

Enter your choice: 3
Search by: 1 (Name)
Enter name to search: Ali
→ Shows all contacts matching 'Ali'


Export to CSV

Enter your choice: 7
→ File saved as: contacts_export_20260608_140022.csv




 Validation & Error Handling

- Empty fields are not allowed
- Email format is validated (must be valid format)
- Phone number is validated (minimum 7 digits)
- Duplicate emails are rejected
- Delete requires confirmation
- All errors handled with try/except blocks



 Author

"Altaf Ali"  
Python Developer — Task 1 Submission



 License

This project is for educational purposes.

"Demo Video"
https://drive.google.com/file/d/1W_D65bMajEGK4cDKpokkR3AnFhVgPm5h/view?usp=sharing
