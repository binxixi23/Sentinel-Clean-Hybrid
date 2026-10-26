# SentinelClean-Hybrid: Autonomous Intelligent Commercial Wet-Dry Maintenance Framework

![SentinelClean Architecture](sentinelcleanaimt.png)

**Course:** ITAI 1378 Computer Vision and AI (Houston City College)  
**Assignment:** Final Capstone Project Production Build  
**Team Member:** Cuong Dang (Individual Project)  
**Project Track:** Option B (Student-Proposed Custom Project)  

---

## 🎯 Project Overview & Market Pivot
Standard robotic vacuums—including high-end consumer appliances like the \$899.99 Roborock QX Revo Ultra 2—feature powerful suction parameters but remain fundamentally incapable of directly vacuuming severe liquid spills. Forcing traditional mechanical configurations over expansive liquid pooling sucks water straight into dry HEPA containment chambers, destroying internal filters, damaging vacuum motors, and dragging cross-contamination mud patterns across clean household boundaries.

**SentinelClean-Hybrid** introduces a disruptive, privacy-first, edge-vision solution to this challenge. Utilizing a localized **YOLOv11** object detection engine alongside an adaptive **ROS2 master state switcher**, the system isolates floor hazards, dynamically alters machine states, and deploys a custom retractable extraction mechanism. 

### 💼 High-Margin Consumable Business Model
Moving past low-margin standalone hardware, this architecture adopts a highly profitable **"Razor and Blades" recurring revenue model**. The physical platform is sold at an optimized price point to maximize market reach, while generating stable, high-margin secondary revenue streams through proprietary single-use high-absorption cotton pad roll replacements over the hardware's operational lifecycle.

---

## 🦅 Core Engineering Specifications

### 1. Retractable "Landing Gear" Extraction Assembly
To eliminate cross-contamination variables, the vehicle features an active mechanical deployment configuration:
* **Chassis Isolation:** The wet-extraction module remains locked in an elevated home orientation above the floor during standard dry-debris sweeping tasks.
* **Servo Actuation:** Upon verification of fluid boundaries, a high-torque RC servo motor (MG996R configuration) rotates an explicit lead screw linkage, dropping the wet extraction array to the floor.
* **Single-Use Containment:** Liquid is pulled directly into specialized disposable cotton pads, containing the mess instantly.

### 2. Algorithmic System Workflow
```unset
[Live Camera Stream] ➡ [Volatile RAM Preprocessing] ➡ [YOLOv11 Inference] ➡ [ROS2 State Switcher] ➡ [Retractable Servo Deployment] ➡ [LED Maintenance Alert]
```

### 3. Multi-Class Object Taxonomy Configuration
The model drops single-class boundaries to map overall household context using the authenticated `v8-spill/liquid-spill-v2` dataset:
* `liquid_spill` (Class ID 0): Safely triggers dry motor shutdown and servo landing gear deployment.
* `dry_debris` (Class ID 1): Maintains regular vacuum configurations at full load.
* `pet_obstacle` (Class ID 2): Triggers immediate navigation detours to avoid collisions.
* `charging_dock` (Class ID 3): Serves as the localized infrastructure anchor point for recovery routing.

---

## 📊 Phase 3 Performance Metrics

### Localized Inference Turning-Point Latency Budget
The frozen PyTorch graph was benchmarked locally on CPU hardware to verify real-time processing performance:
* **Image Matrix Preprocessing:** 4.22 ms  
* **YOLOv11 Core Forward Pass:** 24.15 ms  
* **Non-Maximum Suppression (NMS) Culling:** 2.11 ms  
* **Total Localized Inference Latency:** **30.48 ms**  

*This performance keeps the execution profile safely under our maximum system envelope (< 45.00 ms), leaving an open 14.52 ms processing margin for ROS2 state manipulation task layers.*

---

## 🧠 AI Usage Log
Consistent developmental audit trails, verification prompt structures, and optimization pathways are fully documented in `docs/AI_usage_log.md`.
