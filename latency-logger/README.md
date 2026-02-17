# Latency Logger – Telecom Network Baseline Tool

A lightweight Python tool for measuring network latency (RTT) using ICMP ping and logging results to CSV.

## Purpose

Reliable latency measurement is essential when analysing:

- ISP performance
- Backbone behaviour
- Packet delay and jitter patterns
- Future satellite vs terrestrial comparisons (Starlink Lab)

This tool establishes baseline RTT metrics that can later be compared across networks.

## Features

- Periodic ping to target host
- CSV logging with timestamps
- Success / failure tracking
- Basic summary statistics (min, avg, max, median)

## Example Usage

```bash
python latency_logger.py --host 8.8.8.8 --interval 1 --count 60
