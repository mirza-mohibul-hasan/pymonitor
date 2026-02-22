# pymonitor

A lightweight Python tool that monitors running processes and logs those using high amounts of memory to a CSV file. Useful for identifying memory-heavy applications and tracking usage over time.

## Features

- Monitors all running processes and aggregates memory by process name
- Logs processes using ≥ 500 MB of memory to CSV
- Runs continuously at configurable intervals (default: every 5 seconds)
- Prints entries to the console as they are logged
- Cross-platform (Windows, Linux, macOS)

## Requirements

- Python 3.14+
- [psutil](https://pypi.org/project/psutil/) – for process and system information

## Installation

1. Clone or download this project.

2. Install dependencies with [uv](https://docs.astral.sh/uv/):

   ```bash
   uv sync
   ```

   This creates a virtual environment and installs dependencies from `pyproject.toml`.

## Usage

Run the monitor:

```bash
uv run main.py
```

Or, with the virtual environment activated after `uv sync`:

```bash
python main.py
```

The script will:

- Create `high_memory_apps.csv` if it does not exist
- Print a startup message: `Monitoring apps using >= 500 MB...`
- Every 5 seconds, scan processes and log those using ≥ 500 MB
- Print each logged entry: `YYYY-MM-DD HH:MM:SS | process_name.exe | XXX.XX MB`
- Write all entries to `high_memory_apps.csv`

Stop the monitor with `Ctrl+C`.

## Output Format

`high_memory_apps.csv` has three columns:

| Column           | Description                          |
|------------------|--------------------------------------|
| `timestamp`      | Date and time of the log entry       |
| `process_name`   | Name of the process (e.g. `chrome.exe`) |
| `total_memory_mb`| Total memory used in MB (all instances combined) |

## Configuration

Edit these constants at the top of `main.py`:

| Constant             | Default | Description                          |
|----------------------|---------|--------------------------------------|
| `LOG_FILE`           | `high_memory_apps.csv` | Output CSV filename        |
| `LOG_INTERVAL`       | `5`     | Seconds between scans                |
| `MEMORY_THRESHOLD_MB`| `500`   | Minimum memory (MB) to log a process |

## Example Output

```
Monitoring apps using >= 500 MB...
2026-02-23 05:52:52 | Cursor.exe | 2519.01 MB
2026-02-23 05:52:52 | msedge.exe | 1291.41 MB
2026-02-23 05:52:52 | svchost.exe | 951.86 MB
2026-02-23 05:52:52 | chrome.exe | 1516.2 MB
```

## Note on Permissions

On some systems, you may need elevated permissions to inspect all processes. Access to some processes may be denied and those will be skipped automatically.
