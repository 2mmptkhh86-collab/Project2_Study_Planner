# Simple explanation of Study Planner

- `main.py` creates the window, manager, and CSV storage and connects them.
- `model.py` contains the task rules. It can add, change, finish, search, or delete a task.
- `gui.py` creates the text boxes, buttons, and table you see on screen.
- `controller.py` tells the program what to do when a button is clicked.
- `storage.py` writes tasks into a CSV file and reads them when the program starts.

## Important parts to understand

1. `__init__` sets up a new object.
2. `self._tasks` is the list of tasks inside the manager.
3. `check_input()` checks that the course and task are not empty, the date is real, and the priority is on the list.
4. `add()` gives the new task a number so you can select it later.
5. `edit()` updates the selected task.
6. `toggle_done()` changes between To Do and Done.
7. `search()` shows tasks matching the words in the search box.
8. `load()` and `save()` read and write the CSV file.
9. `try` and `except` catch errors and display a message instead of crashing.

## Try these changes yourself

- Change the window title in `gui.py`.
- Add a fourth priority option, then update validation in `model.py`.
- Add a filter to show only completed tasks.
- Add a new test for your change.

Before using this draft for class, check the AI/source requirements in README.md.
