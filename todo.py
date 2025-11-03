import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

FILE = "TODO.csv"

#Utility Functions
def load_tasks():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        return df
    else:
        return pd.DataFrame(columns=["Task", "Category", "Description", "Status"])

def save_tasks(df):
    df.to_csv(FILE, index=False)

# Core Functionalities
def add_task(event=None):
    task = task_entry.get().strip()
    category = category_entry.get().strip()
    desc = desc_entry.get().strip()

    if not task:
        messagebox.showwarning("Warning", "Task name cannot be empty!")
        return

    df = load_tasks()
    new_row = {"Task": task, "Category": category, "Description": desc, "Status": "Incomplete"}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_tasks(df)
    clear_entries()
    show_tasks()
    messagebox.showinfo("Success", f"Task '{task}' added successfully!")

def show_tasks():
    # Clear previous items
    for row in tree.get_children():
        tree.delete(row)

    df = load_tasks()

    if df.empty:
        return

    df["Status"] = df["Status"].fillna("Incomplete")
    df["sort_order"] = df["Status"].apply(lambda x: 0 if str(x).lower() == "incomplete" else 1)
    df = df.sort_values(by="sort_order", ascending=True).drop(columns="sort_order")

    for i, (_, row) in enumerate(df.iterrows()):
        status = str(row["Status"]).lower()
        tag = "complete" if status == "complete" else "incomplete"
        alt_tag = "alt" if i % 2 == 0 else ""
        tree.insert("", tk.END, values=list(row), tags=(tag, alt_tag))

def mark_complete():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to mark as complete.")
        return

    values = tree.item(selected, "values")
    task_name = values[0]

    df = load_tasks()
    if task_name in df["Task"].values:
        df.loc[df["Task"] == task_name, "Status"] = "Complete"
        save_tasks(df)
        show_tasks()
        messagebox.showinfo("Success", f"Task '{task_name}' marked as complete!")

def delete_task():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        return

    values = tree.item(selected, "values")
    task_name = values[0]

    confirm = messagebox.askyesno("Confirm Delete", f"Delete task '{task_name}'?")
    if confirm:
        df = load_tasks()
        df = df[df["Task"] != task_name]
        save_tasks(df)
        show_tasks()
        messagebox.showinfo("Deleted", f"Task '{task_name}' deleted successfully!")

def clear_entries():
    task_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    task_entry.focus()

def edit_task():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to edit.")
        return

    values = tree.item(selected, "values")
    task_name, cat, desc, status = values

    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Task - {task_name}")
    edit_window.geometry("400x300")
    edit_window.config(bg="#2e2e2e")

    tk.Label(edit_window, text="Edit Task Details", font=("Helvetica", 14, "bold"), bg="#2e2e2e", fg="white").pack(pady=10)

    frame = tk.Frame(edit_window, bg="#2e2e2e")
    frame.pack(pady=10)

    labels = ["Task:", "Category:", "Description:", "Status:"]
    for i, text in enumerate(labels):
        tk.Label(frame, text=text, bg="#2e2e2e", fg="white").grid(row=i, column=0, padx=5, pady=5, sticky="e")

    task_var = tk.StringVar(value=task_name)
    cat_var = tk.StringVar(value=cat)
    desc_var = tk.StringVar(value=desc)
    status_var = tk.StringVar(value=status)

    task_entry_e = tk.Entry(frame, textvariable=task_var, width=30)
    cat_entry_e = tk.Entry(frame, textvariable=cat_var, width=30)
    desc_entry_e = tk.Entry(frame, textvariable=desc_var, width=30)
    status_combo = ttk.Combobox(frame, textvariable=status_var, values=["Incomplete", "Complete"], width=28, state="readonly")

    task_entry_e.grid(row=0, column=1, padx=5, pady=5)
    cat_entry_e.grid(row=1, column=1, padx=5, pady=5)
    desc_entry_e.grid(row=2, column=1, padx=5, pady=5)
    status_combo.grid(row=3, column=1, padx=5, pady=5)

    def save_edit_popup():
        new_task = task_var.get().strip()
        new_cat = cat_var.get().strip()
        new_desc = desc_var.get().strip()
        new_status = status_var.get().strip()

        if not new_task:
            messagebox.showwarning("Warning", "Task name cannot be empty!", parent=edit_window)
            return

        df = load_tasks()
        df.loc[df["Task"] == task_name, ["Task", "Category", "Description", "Status"]] = [new_task, new_cat, new_desc, new_status]
        save_tasks(df)
        show_tasks()
        messagebox.showinfo("Updated", f"Task '{task_name}' updated successfully!", parent=edit_window)
        edit_window.destroy()

    tk.Button(edit_window, text="Save Changes", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
              activebackground="#66BB6A", activeforeground="white",
              command=save_edit_popup).pack(pady=15)

# GUI Layout
root = tk.Tk()
root.title("TODO List by Chiranjit Roy")
root.geometry("850x700")
root.minsize(700, 650)
root.config(bg="#222222")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2d2d2d", fieldbackground="#2d2d2d", foreground="white", rowheight=28, font=("Segoe UI", 10))
style.map("Treeview", background=[("selected", "#4a90e2")])

# Title
title = tk.Label(root, text="📝 TODO Manager", font=("Helvetica", 22, "bold"), bg="#222222", fg="white")
title.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="#222222")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Task:", bg="#222222", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Label(input_frame, text="Category:", bg="#222222", fg="white", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Label(input_frame, text="Description:", bg="#222222", fg="white", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="e")

task_entry = tk.Entry(input_frame, width=45, font=("Segoe UI", 10))
category_entry = tk.Entry(input_frame, width=45, font=("Segoe UI", 10))
desc_entry = tk.Entry(input_frame, width=45, font=("Segoe UI", 10))

task_entry.grid(row=0, column=1, padx=8, pady=5)
category_entry.grid(row=1, column=1, padx=8, pady=5)
desc_entry.grid(row=2, column=1, padx=8, pady=5)

add_button = tk.Button(input_frame, text="➕ Add Task", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                       activebackground="#66BB6A", activeforeground="white",
                       relief="flat", width=20, command=add_task)
add_button.grid(row=3, column=1, columnspan=2, pady=10)

root.bind('<Return>', add_task)


# Treeview Frame with Scrollbars
tree_frame = tk.Frame(root, bg="#222222")
tree_frame.pack(pady=10, fill="both", expand=True)

columns = ("Task", "Category", "Description", "Status")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(yscroll=vsb.set, xscroll=hsb.set)

vsb.pack(side="right", fill="y")
hsb.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180)

# Color tags
tree.tag_configure("complete", background="#3c6e47", foreground="white")
tree.tag_configure("incomplete", background="#3b3b3b", foreground="white")
tree.tag_configure("alt", background="#2b2b2b")

# Buttons
button_frame = tk.Frame(root, bg="#222222")
button_frame.pack(pady=10)

def make_button(text, color, command):
    return tk.Button(button_frame, text=text, bg=color, fg="white", font=("Arial", 10, "bold"),
                     activebackground=color, activeforeground="white", relief="flat", width=16, command=command)

mark_button = make_button("Mark Complete", "#2196F3", mark_complete)
edit_button = make_button("Edit Task", "#FF9800", edit_task)
delete_button = make_button("Delete Task", "#f44336", delete_task)
refresh_button = make_button("Refresh", "#9C27B0", show_tasks)

mark_button.grid(row=0, column=0, padx=10)
edit_button.grid(row=0, column=1, padx=10)
delete_button.grid(row=0, column=2, padx=10)
refresh_button.grid(row=0, column=3, padx=10)

# Hover effect for buttons
def on_enter(e):
    e.widget.config(bg="#555555")
def on_leave(e):
    colors = {"Mark Complete": "#2196F3", "Edit Task": "#FF9800", "Delete Task": "#f44336", "Refresh": "#9C27B0"}
    e.widget.config(bg=colors.get(e.widget["text"], "#4CAF50"))

for btn in (mark_button, edit_button, delete_button, refresh_button):
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Load tasks
show_tasks()
task_entry.focus()

root.mainloop()
