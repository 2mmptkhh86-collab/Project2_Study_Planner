"""Check that Study Planner tasks can be saved and reopened."""

import tempfile
import unittest
from pathlib import Path

from model import TaskManager
from storage import TaskStorage


class StorageTests(unittest.TestCase):
    """Test the CSV file storage."""

    def test_save_and_load(self) -> None:
        """Save a task and read it again."""
        with tempfile.TemporaryDirectory() as folder:
            storage = TaskStorage(Path(folder) / "tasks.csv")
            manager = TaskManager()
            manager.add("CYBR", "Lab", "2026-12-10", "High")
            storage.save(manager.all_tasks())
            loaded = storage.load()
            self.assertEqual(loaded[0]["task"], "Lab")
            new_manager = TaskManager()
            new_manager.load_tasks(loaded)
            self.assertEqual(new_manager.find("1")["course"], "CYBR")

    def test_missing_file(self) -> None:
        """An unused planner begins with no tasks."""
        with tempfile.TemporaryDirectory() as folder:
            storage = TaskStorage(Path(folder) / "missing.csv")
            self.assertEqual(storage.load(), [])


if __name__ == "__main__":
    unittest.main()
