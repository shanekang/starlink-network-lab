import subprocess
import csv
import time
from datetime import datetime

TARGET = "8.8.8.8"   # Google DNS
INTERVAL = 10        # seconds between pings
OUTPUT_FILE = "latency_log.csv"


def ping_host(target):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", target],
            capture_output=True,
            text=True
        )

        output = result.stdout

        # Extract latency time
        for line in output.split("\n"):
            if "time=" in line:
                latency = line.split("time=")[1].split(" ")[0]
                return float(latency)

        return None

    except Exception as e:
        print("Ping error:", e)
        return None


def log_latency():
    with open(OUTPUT_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            latency = ping_host(TARGET)

            if latency is not None:
                print(f"[{timestamp}] Latency: {latency} ms")
                writer.writerow([timestamp, latency])
                file.flush()
            else:
                print(f"[{timestamp}] Ping failed")
                writer.writerow([timestamp, "FAILED"])
                file.flush()

            time.sleep(INTERVAL)


if __name__ == "__main__":
    print("Starting Starlink Latency Logger...")
    log_latency()