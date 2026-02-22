import psutil
import time
import csv
import os
from datetime import datetime

LOG_FILE = "high_memory_apps.csv"
LOG_INTERVAL = 5
MEMORY_THRESHOLD_MB = 500


def write_header_if_not_exists():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "process_name",
                "total_memory_mb"
            ])


def get_high_memory_apps():
    process_memory = {}

    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            name = proc.info['name']
            memory = proc.info['memory_info'].rss  # in bytes

            if name not in process_memory:
                process_memory[name] = 0

            process_memory[name] += memory

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Convert to MB and filter by threshold
    high_memory_apps = []
    for name, memory_bytes in process_memory.items():
        memory_mb = memory_bytes / (1024 * 1024)

        if memory_mb >= MEMORY_THRESHOLD_MB:
            high_memory_apps.append((name, round(memory_mb, 2)))

    return high_memory_apps


def log_data():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    high_memory_apps = get_high_memory_apps()

    if not high_memory_apps:
        return  # nothing to log

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        for name, memory_mb in high_memory_apps:
            writer.writerow([timestamp, name, memory_mb])
            print(f"{timestamp} | {name} | {memory_mb} MB")


def main():
    write_header_if_not_exists()
    print(f"Monitoring apps using >= {MEMORY_THRESHOLD_MB} MB...")

    while True:
        log_data()
        time.sleep(LOG_INTERVAL)


if __name__ == "__main__":
    main()
