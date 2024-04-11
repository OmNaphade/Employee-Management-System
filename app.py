import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Masteroman@12",
    database="employee_management"
)
cursor = conn.cursor()

# Create employee table
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    department VARCHAR(255) NOT NULL,
                    salary DECIMAL(10, 2) NOT NULL
                    )''')


# Function to add employee
def add_employee():
    name = name_entry.get()
    department = department_entry.get()
    salary = salary_entry.get()
    cursor.execute("INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)", (name, department, salary))
    conn.commit()
    update_employee_list()
    clear_entries()


# Function to view all employees
def view_employees():
    cursor.execute("SELECT * FROM employees")
    return cursor.fetchall()


# Function to search for an employee
def search_employee():
    name = search_entry.get()
    cursor.execute("SELECT * FROM employees WHERE name=%s", (name,))
    result = cursor.fetchall()
    employee_tree.delete(*employee_tree.get_children())
    if result:
        for employee in result:
            employee_tree.insert('', 'end', values=employee)
    else:
        tk.messagebox.showinfo("No Results", "No employee found with that name.")


# Function to update employee details
def update_employee_salary():
    name = update_name_entry.get()
    new_salary = new_salary_entry.get()
    cursor.execute("UPDATE employees SET salary=%s WHERE name=%s", (new_salary, name))
    conn.commit()
    update_employee_list()


# Function to delete employee
def delete_employee():
    name = delete_name_entry.get()
    cursor.execute("DELETE FROM employees WHERE name=%s", (name,))
    conn.commit()
    update_employee_list()


# Function to update employee list
def update_employee_list():
    employee_tree.delete(*employee_tree.get_children())
    for employee in view_employees():
        employee_tree.insert('', 'end', values=employee)


# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, 'end')
    department_entry.delete(0, 'end')
    salary_entry.delete(0, 'end')


# Create GUI
root = tk.Tk()
root.title("Employee Management System")

# Background Image
bg_image = tk.PhotoImage(file="background.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Add Employee Frame
add_frame = ttk.LabelFrame(root, text="Add Employee")
add_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

name_label = ttk.Label(add_frame, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(add_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

department_label = ttk.Label(add_frame, text="Department:")
department_label.grid(row=1, column=0, padx=5, pady=5)
department_entry = ttk.Entry(add_frame)
department_entry.grid(row=1, column=1, padx=5, pady=5)

salary_label = ttk.Label(add_frame, text="Salary:")
salary_label.grid(row=2, column=0, padx=5, pady=5)
salary_entry = ttk.Entry(add_frame)
salary_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = ttk.Button(add_frame, text="Add Employee", command=add_employee)
add_button.grid(row=3, columnspan=2, padx=5, pady=5)

# Employee List Frame
list_frame = ttk.LabelFrame(root, text="Employee List")
list_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

employee_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Department", "Salary"), show="headings")
employee_tree.heading("ID", text="ID")
employee_tree.heading("Name", text="Name")
employee_tree.heading("Department", text="Department")
employee_tree.heading("Salary", text="Salary")
employee_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=employee_tree.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
employee_tree.configure(yscrollcommand=scrollbar.set)

# Search Frame
search_frame = ttk.LabelFrame(root, text="Search Employee")
search_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

search_label = ttk.Label(search_frame, text="Search Name:")
search_label.grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Search", command=search_employee)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Update Frame
update_frame = ttk.LabelFrame(root, text="Update Employee Salary")
update_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

update_name_label = ttk.Label(update_frame, text="Employee Name:")
update_name_label.grid(row=0, column=0, padx=5, pady=5)
update_name_entry = ttk.Entry(update_frame)
update_name_entry.grid(row=0, column=1, padx=5, pady=5)

new_salary_label = ttk.Label(update_frame, text="New Salary:")
new_salary_label.grid(row=1, column=0, padx=5, pady=5)
new_salary_entry = ttk.Entry(update_frame)
new_salary_entry.grid(row=1, column=1, padx=5, pady=5)

update_button = ttk.Button(update_frame, text="Update Salary", command=update_employee_salary)
update_button.grid(row=2, columnspan=2, padx=5, pady=5)

# Delete Frame
delete_frame = ttk.LabelFrame(root, text="Delete Employee")
delete_frame.grid(row=2, columnspan=2, padx=10, pady=5, sticky="nsew")

delete_name_label = ttk.Label(delete_frame, text="Employee Name:")
delete_name_label.grid(row=0, column=0, padx=5, pady=5)
delete_name_entry = ttk.Entry(delete_frame)
delete_name_entry.grid(row=0, column=1, padx=5, pady=5)

delete_button = ttk.Button(delete_frame, text="Delete Employee", command=delete_employee)
delete_button.grid(row=1, columnspan=2, padx=5, pady=5)

# Configure row and column weights for responsive resizing
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Populate employee list
update_employee_list()

root.mainloop()

# Close connection
conn.close()
