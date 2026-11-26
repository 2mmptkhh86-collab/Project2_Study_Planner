"""Check the Study Planner's task rules without opening the window."""

import unittest

from model import TaskManager


class TaskTests(unittest.TestCase):
    """Test adding, changing, finding, and removing tasks."""

    def setUp(self) -> None:
        """Start each test with an empty task list."""
        self.manager = TaskManager()

    def test_add_task(self) -> None:
        """Add a new task with a unique number."""
        self.manager.add("CSCI", "Finish homework", "2026-12-01", "High")
        self.assertEqual(len(self.manager.all_tasks()), 1)
        self.assertEqual(self.manager.find("1")["status"], "To Do")

    def test_empty_course_and_task(self) -> None:
        """Reject missing names."""
        with self.assertRaises(ValueError):
            self.manager.add("", "Study", "2026-12-01", "Low")
        with self.assertRaises(ValueError):
            self.manager.add("CSCI", "", "2026-12-01", "Low")

    def test_wrong_date(self) -> None:
        """Reject dates that are not real."""
        with self.assertRaises(ValueError):
            self.manager.add("CSCI", "Study", "2026-02-30", "Low")
        with self.assertRaises(ValueError):
            self.manager.add("CSCI", "Study", "next week", "Low")

    def test_wrong_priority(self) -> None:
        """Reject priorities not in the menu."""
        with self.assertRaises(ValueError):
            self.manager.add("CSCI", "Study", "2026-12-01", "Urgent")

    def test_edit_task(self) -> None:
        """Change an existing task."""
        self.manager.add("CSCI", "Old", "2026-12-01", "Low")
        self.manager.edit("1", "HIST", "New", "2026-12-02", "High")
        self.assertEqual(self.manager.find("1")["task"], "New")

    def test_done_and_undo(self) -> None:
        """Mark a task done and then undo it."""
        self.manager.add("CSCI", "Read", "2026-12-01", "Medium")
        self.manager.toggle_done("1")
        self.assertEqual(self.manager.find("1")["status"], "Done")
        self.manager.toggle_done("1")
        self.assertEqual(self.manager.find("1")["status"], "To Do")

    def test_search_and_delete(self) -> None:
        """Search by course or task and delete an assignment."""
        self.manager.add("CSCI", "Code", "2026-12-01", "Low")
        self.manager.add("HIST", "Read", "2026-12-02", "High")
        self.assertEqual(len(self.manager.search("hist")), 1)
        self.manager.delete("1")
        self.assertEqual(len(self.manager.all_tasks()), 1)

    def test_bad_saved_data(self) -> None:
        """Reject incomplete rows in a saved file."""
        with self.assertRaises(ValueError):
            self.manager.load_tasks([{"id": "1", "course": "CSCI"}])


if __name__ == "__main__":
    unittest.main()
