"""Save and load Study Planner tasks in a CSV file."""

import csv
from pathlib import Path

from model import TaskManager


class TaskStorage:
    """Use a CSV file to remember tasks between sessions."""

    def __init__(self, file_path: Path) -> None:
        """Keep the name and location of the CSV file."""
        self.file_path = file_path

    def load(self) -> list[dict[str, str]]:
        """Read tasks from the CSV file, if it exists."""
        if not self.file_path.exists():
            return []
        try:
            with self.file_path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != list(TaskManager.FIELDS):
                    raise ValueError("The saved tasks file has incorrect columns.")
                rows = list(reader)
                if any(None in row or None in row.values() for row in rows):
                    raise ValueError("The saved tasks file has missing values.")
                return rows
        except (OSError, UnicodeError, csv.Error) as error:
            raise OSError("Could not read the saved tasks file.") from error

    def save(self, tasks: list[dict[str, str]]) -> None:
        """Write the tasks to a CSV file."""
        try:
            self.file_path.parent.mkdir(exist_ok=True, parents=True)
            with self.file_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=TaskManager.FIELDS)
                writer.writeheader()
                writer.writerows(tasks)
        except (OSError, csv.Error) as error:
            raise OSError("Could not save the tasks file.") from error
