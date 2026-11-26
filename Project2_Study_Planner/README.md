# Project 2 - Study Planner

A simple Python program that helps students keep track of homework.

## What you can do

- Add a course name, homework task, due date, and priority.
- Select a task to edit it.
- Mark a task done or change it back to To Do.
- Delete a task.
- Search for tasks by course or name.
- Save tasks in a CSV file so they are there when the program is opened again.
- See an error message for missing details or an incorrect date.

## How to run it in PyCharm

1. Open the **Project2_Study_Planner** folder in PyCharm.
2. Right-click **main.py** and choose **Run 'main'**.
3. Add a task and close the program. Reopen it to check that the task was saved.

This program uses **Tkinter**, which is included with most regular Python installations. You should not need to install any packages. If your version of Python has no Tkinter, use a Python installation that includes it.

To run the tests, open the PyCharm Terminal and enter:

```bash
python -m unittest discover -s tests -v
```

## Files explained

| File | What it does |
| --- | --- |
| `main.py` | Starts the program |
| `model.py` | Checks input and changes tasks |
| `gui.py` | Makes the window and buttons |
| `controller.py` | Connects the buttons to the code |
| `storage.py` | Saves tasks to `data/tasks.csv` |
| `tests/` | Checks the important functions |

## Notes for class use

This is a ChatGPT-assisted example project. Your professor permits AI help for **some** code, requires you to disclose it at the progress meeting, and requires comments identifying where outside code help was used. The draft is not a final submission as-is. Make meaningful changes yourself, add accurate source comments in the code you use, and be ready to explain and edit it in a live meeting.

Follow any instructions or changes your professor gives at the progress meeting.
