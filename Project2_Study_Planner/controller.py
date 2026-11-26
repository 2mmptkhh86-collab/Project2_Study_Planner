"""Connect the Study Planner buttons to the task rules."""

from typing import Callable

from gui import PlannerWindow
from model import TaskManager
from storage import TaskStorage


class PlannerController:
    """Handle button clicks and keep the task list updated."""

    def __init__(self, window: PlannerWindow, manager: TaskManager, storage: TaskStorage) -> None:
        """Connect each button to the matching function."""
        self.window = window
        self.manager = manager
        self.storage = storage
        window.add_button.configure(command=self.add_task)
        window.edit_button.configure(command=self.edit_task)
        window.done_button.configure(command=self.mark_done)
        window.delete_button.configure(command=self.delete_task)
        window.clear_button.configure(command=window.clear_form)
        window.table.bind("<<TreeviewSelect>>", self.select_task)
        window.search_var.trace_add("write", self.search_changed)
        self.refresh()

    def refresh(self) -> None:
        """Show matching tasks after each change."""
        tasks = self.manager.search(self.window.search_var.get())
        self.window.show_tasks(tasks, self.manager.count_text())

    def search_changed(self, *_args: object) -> None:
        """Update the list when the search box changes."""
        self.refresh()

    def select_task(self, _event: object) -> None:
        """Fill the form when the user selects a row."""
        task_id = self.window.selected_id()
        if task_id:
            self.window.show_task(self.manager.find(task_id))

    def save_change(self, action: Callable[[], None]) -> None:
        """Make a change and save it; restore old tasks if saving fails."""
        old_tasks = self.manager.all_tasks()
        try:
            action()
            self.storage.save(self.manager.all_tasks())
        except (ValueError, OSError) as error:
            self.manager.load_tasks(old_tasks)
            self.window.show_error(str(error))
            return
        self.refresh()
        self.window.clear_form()

    def add_task(self) -> None:
        """Add a homework task from the form."""
        self.save_change(lambda: self.manager.add(*self.window.form_values()))

    def edit_task(self) -> None:
        """Save changes to the selected task."""
        task_id = self.window.selected_id()
        self.save_change(lambda: self.manager.edit(task_id, *self.window.form_values()))

    def mark_done(self) -> None:
        """Change the selected task between Done and To Do."""
        task_id = self.window.selected_id()
        self.save_change(lambda: self.manager.toggle_done(task_id))

    def delete_task(self) -> None:
        """Delete the selected task."""
        task_id = self.window.selected_id()
        self.save_change(lambda: self.manager.delete(task_id))
