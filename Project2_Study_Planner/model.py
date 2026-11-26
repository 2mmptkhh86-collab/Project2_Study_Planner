"""Store homework tasks and check the user's input."""

from datetime import date


class TaskManager:
    """Keep a list of tasks and change them when asked."""

    FIELDS = ("id", "course", "task", "due", "priority", "status")

    def __init__(self) -> None:
        """Start with an empty list."""
        self._tasks: list[dict[str, str]] = []

    @staticmethod
    def check_input(course: str, task: str, due: str, priority: str) -> tuple[str, str, str, str]:
        """Check the course, task, due date, and priority."""
        course = course.strip()
        task = task.strip()
        due = due.strip()

        if not course or not task:
            raise ValueError("Enter a course and a task name.")
        if len(course) > 50 or len(task) > 100:
            raise ValueError("Course or task name is too long.")
        try:
            real_date = date.fromisoformat(due)
        except ValueError:
            raise ValueError("Date must be real and written YYYY-MM-DD.") from None
        if real_date.isoformat() != due:
            raise ValueError("Use the date format YYYY-MM-DD.")
        if priority not in ("Low", "Medium", "High"):
            raise ValueError("Choose Low, Medium, or High priority.")
        return course, task, due, priority

    def load_tasks(self, rows: list[dict[str, str]]) -> None:
        """Load saved tasks, but reject incorrect saved data."""
        loaded = []
        used_ids = set()
        for row in rows:
            if set(row) != set(self.FIELDS):
                raise ValueError("The saved tasks file has incorrect columns.")
            if not row["id"].isdigit() or int(row["id"]) < 1 or row["id"] in used_ids:
                raise ValueError("The saved tasks file has an invalid task number.")
            self.check_input(row["course"], row["task"], row["due"], row["priority"])
            if row["status"] not in ("To Do", "Done"):
                raise ValueError("The saved tasks file has an invalid status.")
            used_ids.add(row["id"])
            loaded.append(row.copy())
        self._tasks = loaded

    def all_tasks(self) -> list[dict[str, str]]:
        """Return copies of the tasks for saving."""
        return [row.copy() for row in self._tasks]

    def add(self, course: str, task: str, due: str, priority: str) -> None:
        """Add one new homework task."""
        course, task, due, priority = self.check_input(course, task, due, priority)
        numbers = [int(row["id"]) for row in self._tasks]
        next_id = max(numbers, default=0) + 1
        self._tasks.append({"id": str(next_id), "course": course, "task": task,
                            "due": due, "priority": priority, "status": "To Do"})

    def find(self, task_id: str) -> dict[str, str]:
        """Find a task by its number."""
        for row in self._tasks:
            if row["id"] == task_id:
                return row
        raise ValueError("Select a task from the list first.")

    def edit(self, task_id: str, course: str, task: str, due: str, priority: str) -> None:
        """Change the selected task."""
        course, task, due, priority = self.check_input(course, task, due, priority)
        row = self.find(task_id)
        row.update({"course": course, "task": task, "due": due, "priority": priority})

    def toggle_done(self, task_id: str) -> None:
        """Mark a task done, or change it back to To Do."""
        row = self.find(task_id)
        row["status"] = "Done" if row["status"] == "To Do" else "To Do"

    def delete(self, task_id: str) -> None:
        """Delete the selected task."""
        self.find(task_id)
        self._tasks = [row for row in self._tasks if row["id"] != task_id]

    def search(self, words: str) -> list[dict[str, str]]:
        """Find tasks containing the search words."""
        words = words.strip().lower()
        matches = [row for row in self._tasks
                   if words in row["course"].lower() or words in row["task"].lower()]
        return sorted(matches, key=lambda row: (row["status"] == "Done", row["due"]))

    def count_text(self) -> str:
        """Give the number of tasks completed and not completed."""
        done = sum(row["status"] == "Done" for row in self._tasks)
        return f"Total: {len(self._tasks)}    Done: {done}    To Do: {len(self._tasks) - done}"
