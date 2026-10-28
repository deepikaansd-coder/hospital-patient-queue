# Hospital Patient Waiting System

A beginner-friendly CustomTkinter desktop application that demonstrates a first-in, first-out (FIFO) patient queue. Registration assigns a token, **Call Next Patient** removes the front patient, and **Peek Next Patient** shows the front patient without removing them. The queue is an in-memory linked list, so data resets when the application closes.

## Run in this workspace (Windows PowerShell)

This workspace already has a Python 3.13 environment with CustomTkinter installed. Open PowerShell and run:

```powershell
cd E:\Deepikaa\hospital-patient-queue
uv run --no-project --python .\.venv313\Scripts\python.exe .\main.py
```

You can also use **Terminal → Run Task → Run Hospital Patient Waiting System** in VS Code. Close the application window to stop it.

## Set up a fresh copy

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if needed. From the project folder, let uv install Python 3.13, create the environment, and install the dependency:

```powershell
uv python install 3.13
uv venv --python 3.13 .venv313
uv pip install --python .\.venv313\Scripts\python.exe -r .\requirements.txt
uv run --no-project --python .\.venv313\Scripts\python.exe .\main.py
```

The environment does not need to be activated. `uv run` selects its Python interpreter explicitly.

## Test the queue logic

```powershell
uv run --no-project --python .\.venv313\Scripts\python.exe python -m unittest discover -s tests -v
```

The `core/` package contains patient data, the FIFO queue, and registration rules. The `ui/` package contains the window and reusable visual components. Queue data is kept in memory and resets when the app closes.
