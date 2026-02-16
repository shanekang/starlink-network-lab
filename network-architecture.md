# Starlink Network Architecture Overview

## 1. High-Level Architecture

Starlink is a Low Earth Orbit (LEO) satellite internet system.

User Terminal (Dish)
        ↓
LEO Satellite (~550km altitude)
        ↓
Ground Station (Gateway)
        ↓
Starlink Backbone Network
        ↓
Public Internet

---

## 2. Key Components

### 🛰 LEO Satellites
- Operate at low altitude (~550km)
- Lower latency compared to GEO satellites
- Communicate with ground stations and possibly via inter-satellite laser links

### 📡 User Terminal (Dish)
- Phased-array antenna
- Automatically aligns with satellites
- Connects to home router

### 🌍 Ground Station
- Connects satellite traffic to terrestrial fiber backbone
- Acts as gateway to the public internet

---

## 3. Networking Characteristics

- Likely uses CGNAT (Carrier-Grade NAT)
- Public IP may not be directly assigned
- Latency typically 20–50 ms (varies)
- Dynamic routing depending on satellite position

---

## 4. Security Considerations

- Encrypted satellite communication
- NAT limitations for inbound services
- Potential exposure to ISP-level monitoring
- Importance of firewall configuration on local network

---

## 5. Future Experiments

- Measure latency variation over time
- Perform traceroute analysis
- Capture packet behavior using Wireshark
- Test port forwarding limitations under CGNAT
