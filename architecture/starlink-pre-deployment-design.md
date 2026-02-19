# 📡 Starlink Pre-Deployment Network Architecture Design

## Overview

This document outlines the expected network architecture and security posture prior to Starlink deployment.

The goal is to understand:

- ISP-level routing behaviour
- CGNAT implications
- Satellite-based latency characteristics
- Security exposure before and after installation

This design phase ensures structured validation once the hardware arrives.

---

# 🛰 Expected High-Level Topology

[ End Devices (Laptop / Lab PC) ]
│
▼
[ Starlink Router ]
│
▼
[ Starlink Dish (LEO Satellite) ]
│
▼
[ Ground Station ]
│
▼
[ Starlink Backbone Network ]
│
▼
[ Public Internet ]



---

# 🌍 Network Characteristics

## 1️⃣ Carrier-Grade NAT (CGNAT)

Starlink operates under CGNAT in most regions.

Expected behaviour:

- No publicly routable IPv4 assigned to the end user
- Inbound connections blocked by default
- Port forwarding unavailable
- Reduced external attack surface

Validation after deployment:
- Public IP lookup
- Compare WAN IP vs external IP
- Confirm NAT type

---

## 2️⃣ LEO Satellite Architecture

Unlike GEO satellites (~600ms latency), Starlink uses Low Earth Orbit (LEO) satellites.

Expected latency range:
- 20–60ms average
- Potential jitter during satellite handoff
- Dynamic routing through ground stations

Research focus:
- Satellite-to-ground station switching
- Backbone ASN path mapping
- Traceroute pattern analysis

---

## 3️⃣ Expected Routing Behaviour

Hypothesis:

1. Client → Starlink Router
2. Router → Satellite
3. Satellite → Ground Station
4. Ground Station → Starlink ASN
5. Transit → Public Internet

Post-deployment validation tests:
- Traceroute analysis
- ASN lookup
- GeoIP path inspection
- MTU discovery

---

# 🔐 Security Considerations

## Baseline Security Assumptions

- NAT provides inbound filtering
- No direct public exposure expected
- Router interface must be secured

## Hardening Checklist (Planned)

- Disable UPnP (if configurable)
- Strong admin credentials
- Firmware update verification
- Monitor external exposure via Shodan
- Perform external port scan test

---

# 📊 Planned Validation Experiments

After hardware arrival:

- [ ] Confirm CGNAT status
- [ ] Capture baseline latency
- [ ] Measure packet loss
- [ ] Record jitter behaviour
- [ ] Identify ASN ownership
- [ ] Compare performance with mobile hotspot baseline

---

# 🎯 Long-Term Lab Goals

- Compare terrestrial vs satellite routing
- Analyze backbone-level architecture
- Study telecom security implications
- Evaluate attack surface differences
- Develop telecom-focused threat modelling

---

This document represents the pre-deployment architecture phase of the Starlink Network Lab project.

