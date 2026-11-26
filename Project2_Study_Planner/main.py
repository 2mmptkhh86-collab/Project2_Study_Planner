"""Start the Study Planner program."""

from pathlib import Path
from tkinter import messagebox

from controller import PlannerController
from gui import PlannerWindow
from model import TaskManager
from storage import TaskStorage


def main() -> None:
    """Open the window and connect the program parts."""
    window = PlannerWindow()
    manager = TaskManager()
    folder = Path(__file__).resolve().parent
    storage = TaskStorage(folder / "data" / "tasks.csv")

    try:
        manager.load_tasks(storage.load())
    except (ValueError, OSError) as error:
        messagebox.showerror("File Error", str(error), parent=window)
        window.destroy()
        return

    controller = PlannerController(window, manager, storage)
    window.controller = controller
    window.mainloop()


if __name__ == "__main__":
    main()
