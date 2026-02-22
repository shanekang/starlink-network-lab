# Latency Analysis – Telecom Network Insight Module

This module processes and analyses latency data collected from the `latency-logger` tool.

It transforms raw RTT measurements into meaningful performance insights suitable for telecom and satellite network evaluation.

---

## 🎯 Purpose

Reliable latency analytics are critical for:

- ISP performance validation
- Satellite vs terrestrial comparison (Starlink vs nbn)
- Detecting jitter and packet instability
- Establishing long-term network baselines
- Identifying peak-hour congestion patterns

This module represents the **analysis layer** of the Starlink Network Lab data pipeline.

---

## 🏗 Architecture Position

Data Flow:

Latency Logger (ICMP collection)
        ↓
CSV Data Storage
        ↓
Latency Analysis Module
        ↓
Statistical Summary + Visualisation

This separation ensures clean modular design between data collection and data processing.

---

## 📊 Metrics Calculated

- Minimum RTT
- Maximum RTT
- Average RTT
- Median RTT
- Standard Deviation
- Jitter (Δ between consecutive RTT samples)
- Packet loss rate

---

## 📁 Expected Input

CSV file generated from:
