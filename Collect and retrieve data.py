import tkinter as tk
import sqlite3
from tkinter import messagebox


# Initialize the database and create the table
def initialize_database():
    # Connect to SQLite database (recreate if exists)
    conn = sqlite3.connect('person_details.db')
    c = conn.cursor()

    # Drop table if exists (to clear previous data)
    c.execute('''DROP TABLE IF EXISTS persons''')

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    aadhaar_card TEXT,
                    pan_card TEXT,
                    mobile_number TEXT
                )''')

    conn.commit()
    conn.close()


# Function to save person details to the database and clear fields
def save_to_database(event=None):
    # Connect to SQLite database
    conn = sqlite3.connect('person_details.db')
    c = conn.cursor()

    # Retrieve input values
    name = name_entry.get()
    surname = surname_entry.get()
    aadhaar_card = aadhaar_entry.get()
    pan_card = pan_entry.get()
    mobile_number = mobile_entry.get()

    # Validate Aadhaar number (only numeric and 12 digits)
    if not aadhaar_card.isdigit() or len(aadhaar_card) != 12:
        messagebox.showerror("Error", "Aadhaar Card should contain 12 numeric digits.")
        return

    # Validate Mobile number (only numeric and 10 digits)
    if not mobile_number.isdigit() or len(mobile_number) != 10:
        messagebox.showerror("Error", "Mobile Number should contain 10 numeric digits.")
        return

    # Validate PAN number format (alphanumeric with specific format)
    if not pan_card.isalnum() or not pan_card.isupper() or len(pan_card) != 10:
        messagebox.showerror("Error",
                             "PAN Card format is incorrect. It should be 10 characters long with uppercase alphanumeric.")
        return

    # Insert data into the table
    c.execute('''INSERT INTO persons (name, surname, aadhaar_card, pan_card, mobile_number)
                 VALUES (?, ?, ?, ?, ?)''', (name, surname, aadhaar_card, pan_card, mobile_number))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Person details saved successfully!")

    # Clear the entry fields after saving
    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    aadhaar_entry.delete(0, tk.END)
    pan_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)

    # Focus on the first name entry field after saving
    name_entry.focus_set()


# Function to retrieve person details from the database
def retrieve_from_database(event=None):
    # Connect to SQLite database
    conn = sqlite3.connect('person_details.db')
    c = conn.cursor()

    # Retrieve input values
    name = name_entry_retrieve.get()
    surname = surname_entry_retrieve.get()

    # Query to retrieve data
    c.execute('''SELECT * FROM persons WHERE name=? AND surname=?''', (name, surname))
    person_data = c.fetchone()

    conn.close()

    if person_data:
        # Display retrieved data
        messagebox.showinfo("Person Details",
                            f"Name: {person_data[1]}\nSurname: {person_data[2]}\nAadhaar Card: {person_data[3]}\nPAN Card: {person_data[4]}\nMobile Number: {person_data[5]}")
        # Clear entry fields after displaying data
        name_entry_retrieve.delete(0, tk.END)
        surname_entry_retrieve.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Person details not found!")

    # Focus on the first name entry field after closing retrieve window
    name_entry_retrieve.focus_set()


# Upload GUI setup
def open_upload_window():
    upload_root = tk.Tk()
    upload_root.title("Upload Person Details")

    tk.Label(upload_root, text="Name: ").grid(row=0, column=0)
    global name_entry, surname_entry, aadhaar_entry, pan_entry, mobile_entry
    name_entry = tk.Entry(upload_root)
    name_entry.grid(row=0, column=1)
    name_entry.bind('<Return>', lambda event: surname_entry.focus_set())  # Move focus to surname on Enter

    tk.Label(upload_root, text="Surname: ").grid(row=1, column=0)
    surname_entry = tk.Entry(upload_root)
    surname_entry.grid(row=1, column=1)
    surname_entry.bind('<Return>', lambda event: aadhaar_entry.focus_set())  # Move focus to Aadhaar on Enter

    tk.Label(upload_root, text="Aadhaar Card: ").grid(row=2, column=0)
    aadhaar_entry = tk.Entry(upload_root)
    aadhaar_entry.grid(row=2, column=1)
    aadhaar_entry.bind('<Return>', lambda event: pan_entry.focus_set())  # Move focus to PAN on Enter

    tk.Label(upload_root, text="PAN Card: ").grid(row=3, column=0)
    pan_entry = tk.Entry(upload_root)
    pan_entry.grid(row=3, column=1)
    pan_entry.bind('<Return>', lambda event: mobile_entry.focus_set())  # Move focus to Mobile on Enter

    tk.Label(upload_root, text="Mobile Number: ").grid(row=4, column=0)
    mobile_entry = tk.Entry(upload_root)
    mobile_entry.grid(row=4, column=1)
    mobile_entry.bind('<Return>', lambda event: save_to_database())  # Save details on Enter

    save_button = tk.Button(upload_root, text="Save Details", command=save_to_database)
    save_button.grid(row=5, column=1)

    upload_root.mainloop()


# Retrieve GUI setup
def open_retrieve_window():
    retrieve_root = tk.Tk()
    retrieve_root.title("Retrieve Person Details")

    tk.Label(retrieve_root, text="Name: ").grid(row=0, column=0)
    global name_entry_retrieve, surname_entry_retrieve
    name_entry_retrieve = tk.Entry(retrieve_root)
    name_entry_retrieve.grid(row=0, column=1)
    name_entry_retrieve.bind('<Return>',
                             lambda event: surname_entry_retrieve.focus_set())  # Move focus to surname on Enter

    tk.Label(retrieve_root, text="Surname: ").grid(row=1, column=0)
    surname_entry_retrieve = tk.Entry(retrieve_root)
    surname_entry_retrieve.grid(row=1, column=1)
    surname_entry_retrieve.bind('<Return>', lambda event: retrieve_from_database())  # Retrieve details on Enter

    retrieve_button = tk.Button(retrieve_root, text="Retrieve Details", command=retrieve_from_database)
    retrieve_button.grid(row=2, column=1)

    retrieve_root.mainloop()


# Initialize the database
initialize_database()

# Open upload window first
open_upload_window()

# Open retrieve window after upload window is closed
open_retrieve_window()
