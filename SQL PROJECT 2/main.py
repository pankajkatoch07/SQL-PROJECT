import tkinter as tk
from tkinter import messagebox, StringVar
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Create a students table with name, age, and course fields
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
''')
conn.commit()

# Initialize Tkinter window
root = tk.Tk()
root.title("Student Database Management System")
root.geometry("400x600")
root.configure(bg="#f0f0f0")

# Create StringVar for courses
course_var_add = StringVar()
course_var_update = StringVar()

# Sample courses
courses = ["Mathematics", "Science", "English", "History"]

# Function to add a student
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    course = course_var_add.get()

    if name and age.isdigit() and course:
        c.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, int(age), course))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields with valid data.")

# Function to clear input fields after operations
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    course_var_add.set(courses[0])

# Function to update a student
def update_student():
    name = entry_update_name.get()
    age = entry_update_age.get()
    course = course_var_update.get()

    if name and age.isdigit() and course:
        c.execute("UPDATE students SET age=?, course=? WHERE name=?", (int(age), course, name))
        conn.commit()
        
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Student updated successfully!")
        else:
            messagebox.showwarning("Not Found", "Student not found. Cannot update.")
        
        clear_update_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields with valid data.")

# Function to clear update input fields
def clear_update_entries():
    entry_update_name.delete(0, tk.END)
    entry_update_age.delete(0, tk.END)
    course_var_update.set(courses[0])

# Function to delete a student
def delete_student():
    name = entry_delete_name.get()

    if name:
        c.execute("DELETE FROM students WHERE name=?", (name,))
        conn.commit()
        
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Student deleted successfully!")
        else:
            messagebox.showwarning("Not Found", "Student not found. Cannot delete.")
        
        clear_delete_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")

# Function to clear delete input fields
def clear_delete_entries():
    entry_delete_name.delete(0, tk.END)

# Function to search for a student
def search_student():
    name = entry_search_name.get()

    if name:
        c.execute("SELECT * FROM students WHERE name=?", (name,))
        students = c.fetchall()  # Fetch all records with the matching name
        
        if students:
            # Format all matching student data into a single string
            student_info = "\n".join([f"Name: {student[1]}, Age: {student[2]}, Course: {student[3]}" for student in students])
            messagebox.showinfo("Students Found", student_info)
        else:
            messagebox.showwarning("Not Found", "No students found with this name.")
        
        clear_search_entries()
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")

# Function to clear search input fields
def clear_search_entries():
    entry_search_name.delete(0, tk.END)

# Layout for adding a student
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

tk.Label(frame, text="Add Student", font=('Arial', 14), bg="#f0f0f0").grid(row=0, columnspan=2)

tk.Label(frame, text="Name:", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Age:", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
entry_age = tk.Entry(frame)
entry_age.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="Select Course:", bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5)
course_menu_add = tk.OptionMenu(frame, course_var_add, *courses)
course_menu_add.grid(row=3, column=1, padx=10, pady=5)

tk.Button(frame, text="Add Student", command=add_student).grid(row=4, columnspan=2, pady=10)

# Layout for updating a student
tk.Label(frame, text="Update Student", font=('Arial', 14), bg="#f0f0f0").grid(row=5, columnspan=2)

tk.Label(frame, text="Name:", bg="#f0f0f0").grid(row=6, column=0, padx=10, pady=5)
entry_update_name = tk.Entry(frame)
entry_update_name.grid(row=6, column=1, padx=10, pady=5)

tk.Label(frame, text="New Age:", bg="#f0f0f0").grid(row=7, column=0, padx=10, pady=5)
entry_update_age = tk.Entry(frame)
entry_update_age.grid(row=7, column=1, padx=10, pady=5)

tk.Label(frame, text="Select Course:", bg="#f0f0f0").grid(row=8, column=0, padx=10, pady=5)
course_menu_update = tk.OptionMenu(frame, course_var_update, *courses)
course_menu_update.grid(row=8, column=1, padx=10, pady=5)

tk.Button(frame, text="Update Student", command=update_student).grid(row=9, columnspan=2, pady=10)

# Layout for deleting a student
tk.Label(frame, text="Delete Student", font=('Arial', 14), bg="#f0f0f0").grid(row=10, columnspan=2)

tk.Label(frame, text="Name:", bg="#f0f0f0").grid(row=11, column=0, padx=10, pady=5)
entry_delete_name = tk.Entry(frame)
entry_delete_name.grid(row=11, column=1, padx=10, pady=5)

tk.Button(frame, text="Delete Student", command=delete_student).grid(row=12, columnspan=2, pady=10)

# Layout for searching a student
tk.Label(frame, text="Search Student", font=('Arial', 14), bg="#f0f0f0").grid(row=13, columnspan=2)

tk.Label(frame, text="Name:", bg="#f0f0f0").grid(row=14, column=0, padx=10, pady=5)
entry_search_name = tk.Entry(frame)
entry_search_name.grid(row=14, column=1, padx=10, pady=5)

tk.Button(frame, text="Search Student", command=search_student).grid(row=15, columnspan=2, pady=10)

# Start the Tkinter main loop
root.mainloop()

# Close the database connection
conn.close()
