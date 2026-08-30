# TESDA Pomodoro Timer

A simple desktop Pomodoro-style time management application built with Python and Tkinter. Designed for the TESDA/BARMM office to help ICT focals stay focused through structured work and break sessions.

## Features

- **Pomodoro work timer** — 25-minute focused work sessions
- **Short break** — 5 minutes between work sessions
- **Long break** — 15 minutes after completing your session cycles
- **Custom timer** — run a timer for any number of minutes
- **Task list** — add, mark complete, and save your tasks to a file
- **Finish session** — marks the selected task as completed when a *work* session finishes (breaks never complete tasks)
- **Stop button** — cancel a running timer at any time
- **Cycle counter** — tracks how many work sessions you've completed today

## Requirements

- Python 3.8+ (uses only the standard library — Tkinter and `pathlib`, no external packages)

### Linux Tkinter note

On Ubuntu/Debian Tkinter is not always bundled with Python. Install it with:

```bash
sudo apt install python3-tk
```

## Run

```bash
python3 pomodoroTESD.py
```

## Build an executable (PyInstaller)

A `.spec` file is included. Build a standalone executable with:

```bash
pyinstaller pomodoroTESD.spec
```

The executable is written to `dist/`. Use `pomodoro-technique.ico` / `pomodoro-technique.png` as the icon.

## How it works

- The timer uses `time.monotonic()` and Tk's `after()` for drift-free, thread-safe countdown — no background threads.
- Tasks save to a plain-text file in your **home directory** (`task_log.txt`), so it works on any OS without hardcoding machine-specific paths.
- A work session only offers "Finish Session & Complete Task" once it completes naturally; stopping or running a break never completes a task.

## Project structure

```
pomodoro/
├── pomodoroTESD.py      # The application source
├── pomodoroTESD.spec    # PyInstaller build configuration
├── pomodoro-technique.ico / .png  # App icon
└── README.md
```
