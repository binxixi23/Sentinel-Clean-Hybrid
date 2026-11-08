# SentinelClean-Hybrid: Simple Industrial Sorting System

![SentinelClean Industrial Architecture](sentinelcleanaimt.png)

---

## 🎯 Overview & Business Plan
**SentinelClean-Hybrid** is an automated sorting system for fast industrial conveyor belts. It is faster and better than old infrared sensors or color checks.

* **Main Technology:** Uses a custom **YOLOv26** object detection system built right into the local device. This keeps the work fast without slowing down the main computer.
* **Business Plan:** The project uses a *"Razor and Blades"* model. The main sorting machine is sold cheap to get people to use it. Money is made by selling replaceable single-use cotton filters.

---

## 🗺️ Development Steps
`[Phase 1: Design] ➡ [Phase 2: Data] ➡ [Phase 3: Training] ➡ [Phase 4: State Machine] ➡ [Phase 5: Launch]`

### 📋 Phase 1 & 2: Project Goal & Waste Types
* **Local Processing:** The system runs directly on the local machine instead of sending data to the cloud, making it much faster.
* **3-Class Waste Groups (80% Training, 10% Validation, 10% Testing):**
  * **Class 0: Dry Waste** -> Paper, recyclable items, clean cardboard boxes.
  * **Class 1: Wet Waste** -> Food waste, wet organic materials, damp trash.
  * **Class 2: Liquid Spill** -> Puddles, water, and wet chemical spills (Top priority safety target).

### 🧠 Phase 3 & 4: Training & Automation
* **YOLOv26 Training Results (50 Training Rounds):**
  * `Round 01`: `box_loss: 1.4210 | cls_loss: 2.8180 | mAP50: 0.3200`
  * `Round 25`: `box_loss: 0.9870 | cls_loss: 1.5430 | mAP50: 0.5850`
  * `Round 50`: `box_loss: 0.6924 | cls_loss: 1.0620 | mAP50: 0.6350 -> [Model Saved: best.pt]`
* **System Code (`src/image_preprocessing.py`):** A Python program checks the camera video in real-time and tells the machine what to sort.

```python
import os
import cv2
import numpy as np
import torch
from ultralytics import YOLO

class SentinelCleanConveyorCore:
    def __init__(self, model_path="best.pt"):
        self.CONF_THRESHOLD = 0.25
        self.active_state = "CONVEYOR_PASSIVE_MONITORING"
        if os.path.exists(model_path):
            self.device_target = 0 if torch.cuda.is_available() else "cpu"
            self.model = YOLO(model_path)
            self.model.to(self.device_target)
```

### 📥 Phase 5: Speed, Safety, & Privacy
* **Speed Test Results:**
  * Image Preparation: **4.22 ms**
  * YOLOv26 AI Check: **25.88 ms**
  * System Switcher: **0.04 ms**
  * **Total Time: 30.14 ms** (Faster than the required 45.00 ms industrial limit).
* **Safety Backup Plan:** If the system gets too slow during a busy time, it skips extra frames and focuses only on **Class 2 (`Liquid Spill`)**.
* **Privacy:** All camera video is processed directly in the computer's memory. Nothing is saved to a hard drive or sent to the cloud, keeping factory data safe.

---

## 🧠 AI Development Log
The full history of how this AI was built, along with code prompts and graphs, can be found in `docs/AI_usage_log.md`.
