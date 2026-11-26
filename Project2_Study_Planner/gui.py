"""Build the Study Planner window with Tkinter."""

import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk


class PlannerWindow(tk.Tk):
    """Show the text boxes, buttons, and task list."""

    def __init__(self) -> None:
        """Create the window and its widgets."""
        super().__init__()
        self.title("Study Planner")
        self.geometry("920x570")
        self.resizable(False, False)

        self.course_var = tk.StringVar()
        self.task_var = tk.StringVar()
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.priority_var = tk.StringVar(value="Medium")
        self.search_var = tk.StringVar()
        self.count_var = tk.StringVar(value="Total: 0    Done: 0    To Do: 0")

        self.build_widgets()

    def build_widgets(self) -> None:
        """Place the form, buttons, and task table in the window."""
        ttk.Label(self, text="Study Planner", font=("Arial", 18, "bold")).pack(pady=12)

        form = ttk.LabelFrame(self, text="Homework details", padding=10)
        form.pack(fill="x", padx=15)

        labels = ("Course", "Task", "Due date (YYYY-MM-DD)", "Priority")
        for col, name in enumerate(labels):
            ttk.Label(form, text=name).grid(row=0, column=col, padx=5, sticky="w")

        ttk.Entry(form, textvariable=self.course_var, width=18).grid(row=1, column=0, padx=5)
        ttk.Entry(form, textvariable=self.task_var, width=30).grid(row=1, column=1, padx=5)
        ttk.Entry(form, textvariable=self.date_var, width=20).grid(row=1, column=2, padx=5)
        ttk.Combobox(form, textvariable=self.priority_var, values=("Low", "Medium", "High"),
                     state="readonly", width=12).grid(row=1, column=3, padx=5)

        actions = ttk.Frame(self)
        actions.pack(pady=12)
        self.add_button = ttk.Button(actions, text="Add Task")
        self.edit_button = ttk.Button(actions, text="Edit Selected")
        self.done_button = ttk.Button(actions, text="Done / Undo")
        self.delete_button = ttk.Button(actions, text="Delete Selected")
        self.clear_button = ttk.Button(actions, text="Clear Boxes")
        for button in (self.add_button, self.edit_button, self.done_button,
                       self.delete_button, self.clear_button):
            button.pack(side="left", padx=5)

        search = ttk.Frame(self)
        search.pack(fill="x", padx=15, pady=5)
        ttk.Label(search, text="Search:").pack(side="left")
        ttk.Entry(search, textvariable=self.search_var, width=35).pack(side="left", padx=7)
        ttk.Label(search, textvariable=self.count_var).pack(side="right")

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=15, pady=(6, 15))
        cols = ("id", "course", "task", "due", "priority", "status")
        self.table = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        widths = (45, 120, 260, 120, 100, 85)
        names = ("#", "Course", "Task", "Due Date", "Priority", "Status")
        for col, width, label in zip(cols, widths, names):
            self.table.heading(col, text=label)
            self.table.column(col, width=width, anchor="w")
        bar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=bar.set)
        self.table.pack(side="left", fill="both", expand=True)
        bar.pack(side="right", fill="y")

    def form_values(self) -> tuple[str, str, str, str]:
        """Get what the user entered in the text boxes."""
        return (self.course_var.get(), self.task_var.get(),
                self.date_var.get(), self.priority_var.get())

    def selected_id(self) -> str:
        """Get the number of the chosen row."""
        selected = self.table.selection()
        return selected[0] if selected else ""

    def show_task(self, task: dict[str, str]) -> None:
        """Put the selected task into the boxes for editing."""
        self.course_var.set(task["course"])
        self.task_var.set(task["task"])
        self.date_var.set(task["due"])
        self.priority_var.set(task["priority"])

    def clear_form(self) -> None:
        """Empty the text boxes and clear the selection."""
        self.course_var.set("")
        self.task_var.set("")
        self.date_var.set(date.today().isoformat())
        self.priority_var.set("Medium")
        self.table.selection_remove(self.table.selection())

    def show_tasks(self, tasks: list[dict[str, str]], counts: str) -> None:
        """Show the task list in the table."""
        for item in self.table.get_children():
            self.table.delete(item)
        for task in tasks:
            values = tuple(task[col] for col in ("id", "course", "task", "due", "priority", "status"))
            self.table.insert("", "end", iid=task["id"], values=values)
        self.count_var.set(counts)

    def show_error(self, message: str) -> None:
        """Display a message when something is wrong."""
        messagebox.showerror("Study Planner", message, parent=self)
