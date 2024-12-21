import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def connect_db():
    """Connect to the SQLite database (or create it if it doesn't exist)"""
    conn = sqlite3.connect("records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    return conn

def create_record(conn, name, age, email):
    """Create a new record in the database"""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO records (name, age, email) VALUES (?, ?, ?)", (name, age, email))
        conn.commit()
        messagebox.showinfo("Success", "Record created successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email must be unique.")

def update_record(conn, record_id, name, age, email):
    """Update an existing record"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    if not record:
        messagebox.showerror("Error", "Record not found.")
        return

    try:
        cursor.execute("""
            UPDATE records
            SET name = ?, age = ?, email = ?
            WHERE id = ?
        """, (name, age, email, record_id))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email must be unique.")

def delete_record(conn, record_id):
    """Delete a record by ID"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Record deleted successfully.")
    else:
        messagebox.showerror("Error", "Record not found.")

def display_records(conn, tree):
    """Display all records in the database"""
    for item in tree.get_children():
        tree.delete(item)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    for record in records:
        tree.insert("", "end", values=record)

def main():
    conn = connect_db()

    def create_record_ui():
        def submit():
            name = entry_name.get()
            age = entry_age.get()
            email = entry_email.get()
            if name and age.isdigit() and email:
                create_record(conn, name, int(age), email)
                display_records(conn, tree)
                top.destroy()
            else:
                messagebox.showerror("Error", "Please provide valid inputs.")

        top = tk.Toplevel(root)
        top.title("Add Record")
        top.configure(bg="dodger blue")

        ttk.Label(top, text="Name:", background="dodger blue", foreground="white").grid(row=0, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(top, width=30)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top, text="Age:", background="dodger blue", foreground="white").grid(row=1, column=0, padx=5, pady=5)
        entry_age = ttk.Entry(top, width=30)
        entry_age.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(top, text="Email:", background="dodger blue", foreground="white").grid(row=2, column=0, padx=5, pady=5)
        entry_email = ttk.Entry(top, width=30)
        entry_email.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(top, text="Add", command=submit).grid(row=3, columnspan=2, pady=10)

    def update_record_ui():
        def load_record():
            record_id = entry_id.get()
            if not record_id.isdigit():
                messagebox.showerror("Error", "Please enter a valid ID.")
                return

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records WHERE id = ?", (int(record_id),))
            record = cursor.fetchone()
            if not record:
                messagebox.showerror("Error", "Record not found.")
                return

            entry_name.delete(0, tk.END)
            entry_name.insert(0, record[1])

            entry_age.delete(0, tk.END)
            entry_age.insert(0, record[2])

            entry_email.delete(0, tk.END)
            entry_email.insert(0, record[3])

        def submit():
            record_id = entry_id.get()
            name = entry_name.get()
            age = entry_age.get()
            email = entry_email.get()
            if record_id.isdigit() and name and age.isdigit() and email:
                update_record(conn, int(record_id), name, int(age), email)
                display_records(conn, tree)
                top.destroy()
            else:
                messagebox.showerror("Error", "Please provide valid inputs.")

        top = tk.Toplevel(root)
        top.title("Update Record")
        top.configure(bg="dodger blue")

        ttk.Label(top, text="Record ID:", background="dodger blue", foreground="white").grid(row=0, column=0, padx=5, pady=5)
        entry_id = ttk.Entry(top, width=30)
        entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(top, text="Load", command=load_record).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(top, text="Name:", background="dodger blue", foreground="white").grid(row=1, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(top, width=30)
        entry_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(top, text="Age:", background="dodger blue", foreground="white").grid(row=2, column=0, padx=5, pady=5)
        entry_age = ttk.Entry(top, width=30)
        entry_age.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(top, text="Email:", background="dodger blue", foreground="white").grid(row=3, column=0, padx=5, pady=5)
        entry_email = ttk.Entry(top, width=30)
        entry_email.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(top, text="Update", command=submit).grid(row=4, columnspan=3, pady=10)

    def delete_record_ui():
        def submit():
            record_id = entry_record_id.get()
            if record_id.isdigit():
                delete_record(conn, int(record_id)) 
                display_records(conn, tree)
                top.destroy()
            else:
                messagebox.showerror("Error", "Please enter a valid record ID.")

        top = tk.Toplevel(root)
        top.title("Delete Record")
        top.configure(bg="dodger blue")

        ttk.Label(top, text="Record ID:", background="dodger blue", foreground="white").grid(row=0, column=0, padx=5, pady=5)
        entry_record_id = ttk.Entry(top, width=30) 
        entry_record_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(top, text="Delete", command=submit).grid(row=1, columnspan=2, pady=10)

    root = tk.Tk()
    root.title("Database Application")
    root.configure(bg="dodger blue")

    frame = ttk.Frame(root, padding="10")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Age", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Email", text="Email")
    tree.pack(fill="both", expand=True)

    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), foreground="dodger blue", background="white")

    btn_display = ttk.Button(btn_frame, text="Display All Records", command=lambda: display_records(conn, tree))
    btn_display.pack(side="left", padx=5)

    btn_create = ttk.Button(btn_frame, text="Create Record", command=create_record_ui)
    btn_create.pack(side="left", padx=5)

    btn_update = ttk.Button(btn_frame, text="Update Record", command=update_record_ui)
    btn_update.pack(side="left", padx=5)

    btn_delete = ttk.Button(btn_frame, text="Delete Record", command=delete_record_ui)
    btn_delete.pack(side="left", padx=5)

    display_records(conn, tree)
    root.mainloop()

if __name__ == "__main__":
    main()
