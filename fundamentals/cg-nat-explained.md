# Starlink Home Network Pre-Deployment Design

## 1. Physical Topology
- Starlink Dish
- Starlink Router (Bypass Mode 예정)
- Managed Switch (VLAN 분리 예정)
- Home Lab PC
- IoT Devices
- Guest WiFi

## 2. Logical Segmentation Plan
- VLAN 10 – Main devices
- VLAN 20 – Lab environment
- VLAN 30 – IoT
- VLAN 40 – Guest

## 3. Security Considerations
- Default deny firewall rules
- DNS logging
- Traffic monitoring (Wireshark / tcpdump)
- CGNAT impact analysis

## 4. Testing Plan
- Latency baseline test
- Packet loss test
- Traceroute comparison (nbn vs Starlink)
