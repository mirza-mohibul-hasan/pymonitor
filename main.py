import psutil
import time
import csv
import sys
from datetime import datetime
import os

LOG_FILE = "system_monitor.csv"
LOG_INTERVAL = 1


def write_header_if_not_exists():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "cpu_percent", "memory_percent"])


def log_data():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu, memory])


def main():
    write_header_if_not_exists()
    print("Logging started... Press Ctrl+C to stop.")

    try:
        while True:
            log_data()
            time.sleep(LOG_INTERVAL)
    except KeyboardInterrupt:
        print("\nLogging stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
