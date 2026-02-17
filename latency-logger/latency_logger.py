#!/usr/bin/env python3
"""
Latency Logger (ICMP ping 기반)
- 지정한 호스트에 주기적으로 ping을 보내 RTT(ms)를 CSV로 저장
- Windows/macOS/Linux 동작 (ping 명령어 파싱 방식 포함)
- 종료 시 간단 요약 통계 출력

사용 예:
  python latency_logger.py --host 8.8.8.8 --interval 2 --count 50
  python latency_logger.py --host 1.1.1.1 --interval 1 --duration 300
"""

import argparse
import csv
import os
import platform
import re
import statistics
import subprocess
import sys
import time
from datetime import datetime


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Latency Logger using system ping.")
    p.add_argument("--host", required=True, help="Target host/IP (e.g., 8.8.8.8)")
    p.add_argument("--interval", type=float, default=1.0, help="Seconds between pings (default: 1.0)")
    group = p.add_mutually_exclusive_group(required=False)
    group.add_argument("--count", type=int, help="Number of pings to run (e.g., 100)")
    group.add_argument("--duration", type=int, help="Run duration in seconds (e.g., 300)")
    p.add_argument("--timeout", type=int, default=2, help="Ping timeout seconds (default: 2)")
    p.add_argument("--out", default="", help="Output CSV path. Default auto in ./data/")
    return p.parse_args()


def build_ping_command(host: str, timeout_s: int) -> list[str]:
    system = platform.system().lower()

    # Windows: timeout in ms with -w
    if "windows" in system:
        return ["ping", "-n", "1", "-w", str(timeout_s * 1000), host]

    # macOS/Linux: -c 1, timeout differs:
    # Linux usually supports -W (seconds)
    # macOS uses -W (milliseconds) or -t (ttl) depending; we’ll keep it simple and parse output
    if "linux" in system:
        return ["ping", "-c", "1", "-W", str(timeout_s), host]

    # macOS (Darwin): use -c 1 and rely on system default timeout
    return ["ping", "-c", "1", host]


def extract_rtt_ms(ping_output: str) -> float | None:
    """
    Return RTT in ms if found, else None.
    Handles common formats:
    - "time=12.3 ms"
    - "time<1ms" (Windows)
    """
    # Windows sometimes: time=14ms or time<1ms
    m = re.search(r"time[=<]\s*([0-9.]+)\s*ms", ping_output, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None

    # Some variants: "time=14.2 ms"
    m2 = re.search(r"time=\s*([0-9.]+)\s*ms", ping_output, re.IGNORECASE)
    if m2:
        try:
            return float(m2.group(1))
        except ValueError:
            return None

    return None


def ensure_out_path(out_arg: str, host: str) -> str:
    if out_arg.strip():
        return out_arg.strip()

    os.makedirs("data", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_host = re.sub(r"[^a-zA-Z0-9_.-]", "_", host)
    return os.path.join("data", f"latency_{safe_host}_{ts}.csv")


def write_header_if_new(path: str) -> None:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp_iso", "host", "success", "rtt_ms", "raw"])


def run_ping_once(cmd: list[str]) -> tuple[bool, float | None, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        output = (proc.stdout or "") + (proc.stderr or "")
        rtt = extract_rtt_ms(output)
        success = (proc.returncode == 0) and (rtt is not None)
        return success, rtt, output.strip().replace("\n", " | ")[:500]
    except Exception as e:
        return False, None, f"EXCEPTION: {e}"


def summarize(rtts: list[float]) -> str:
    if not rtts:
        return "No successful RTT samples collected."

    avg = statistics.mean(rtts)
    med = statistics.median(rtts)
    p95 = statistics.quantiles(rtts, n=20)[18] if len(rtts) >= 20 else max(rtts)  # rough p95
    mn = min(rtts)
    mx = max(rtts)
    stdev = statistics.pstdev(rtts) if len(rtts) >= 2 else 0.0

    return (
        f"Samples: {len(rtts)}\n"
        f"Min: {mn:.2f} ms\n"
        f"Avg: {avg:.2f} ms\n"
        f"Median: {med:.2f} ms\n"
        f"P95: {p95:.2f} ms\n"
        f"Max: {mx:.2f} ms\n"
        f"StdDev: {stdev:.2f} ms\n"
    )


def main() -> int:
    args = parse_args()

    out_path = ensure_out_path(args.out, args.host)
    write_header_if_new(out_path)

    cmd = build_ping_command(args.host, args.timeout)

    print(f"[Latency Logger] host={args.host} interval={args.interval}s timeout={args.timeout}s")
    print(f"[Latency Logger] output -> {out_path}")
    print(f"[Latency Logger] ping cmd -> {' '.join(cmd)}")
    print("Press Ctrl+C to stop.\n")

    rtts: list[float] = []
    start = time.time()
    sent = 0

    try:
        while True:
            now = datetime.now().isoformat(timespec="seconds")
            success, rtt, raw = run_ping_once(cmd)
            sent += 1

            if success and rtt is not None:
                rtts.append(rtt)

            with open(out_path, "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow([now, args.host, int(success), (f"{rtt:.2f}" if rtt is not None else ""), raw])

            status = f"OK {rtt:.2f} ms" if success and rtt is not None else "FAIL"
            print(f"{now}  {args.host:<20}  {status}")

            # stop conditions
            if args.count is not None and sent >= args.count:
                break
            if args.duration is not None and (time.time() - start) >= args.duration:
                break

            time.sleep(max(0.0, args.interval))

    except KeyboardInterrupt:
        print("\nStopped by user.\n")

    print(summarize(rtts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
