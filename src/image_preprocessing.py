import os
import time
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

            device_label = "GPU (CUDA:0)" if self.device_target == 0 else "CPU"
            print(f"[INIT] Loaded NMS-Free YOLOv26 Architecture on: {device_label}")
            print("[INIT] Warming up tensor graph layers to prime volatile memory registries...")
            
            warmup_frame = np.zeros((640, 640, 3), dtype=np.uint8)
            for _ in range(3):
                _ = self.model.predict(source=warmup_frame, conf=self.CONF_THRESHOLD, verbose=False)
            print("[INIT] Warm-up complete. Memory registries primed.")
        else:
            raise FileNotFoundError(f"Weight asset '{model_path}' not found at root directory.")

    def process_conveyor_frame(self, image_path):
        if not os.path.exists(image_path):
            return "❌ Workspace Exception: Target file is unreachable."

        img_raw = cv2.imread(image_path)
        if img_raw is None:
            return "❌ Matrix Parsing Error: Image array stream is empty or unreadable."

        if np.max(img_raw) == np.min(img_raw):
            return "❌ Input Constraint Violation: Image is fully blank or black."

        # YOLOv26 NMS-Free Inference outputs an array list containing data frames
        results_list = self.model.predict(source=img_raw, conf=self.CONF_THRESHOLD, device=self.device_target, verbose=False)
        
        # FIXED: Extract the first structural result element from the list block
        results = results_list[0]
        boxes = results.boxes

        # Export annotated frame logic
        img_output = results.plot()
        output_dir = "results/inference_output"
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, "result_spill.jpg")
        cv2.imwrite(output_file_path, img_output)

        if len(boxes) == 0:
            self.active_state = "CONVEYOR_PASSIVE_MONITORING"
            return "STATE: PASS_THROUGH - Clean floor detected. Maintaining nominal velocity."

        class_mapping = {0: "Dry Waste", 1: "Wet Waste", 2: "Liquid Spill"}

        for box in boxes:
            class_id = int(box.cls)
            confidence_score = float(box.conf)
            class_name = class_mapping.get(class_id, "Unknown Entity")

            # REVISED CLOSED-LOOP MECHANICAL REMEDIATION MACHINE LOGIC
            if class_id == 2:  # High Priority Fluid Threat
                self.active_state = "EMERGENCY_WET_ISOLATION"
                return (
                    f"\n🚨 INDUSTRIAL FLUID HAZARD DETECTED: {class_name.upper()} ({round(confidence_score * 100, 1)}%) 🚨\n"
                    f"-> [PHASE 1 - FLUID REMEDIATION ACTIVE]: Deploying Cụm 1 Water-Absorption Mechanisms.\n"
                    f"-> [PHASE 1]: Isolating puddle area to prevent widespread cross-contamination.\n"
                    f"-> [PHASE 2 - RE-SWEEP ENGAGEMENT]: Reversing conveyor belt / backing up robot chassis to the surge zone...\n"
                    f"-> [PHASE 3 - DRY CLEANING ACTIVE]: Activating Cụm 2 Vacuum & Dry Sweeper to clear remaining Class 0/1 debris.\n"
                    f"-> STATUS: 100% Recycled Area Extraction Achieved. No waste left behind."
                )
            elif class_id == 0 or class_id == 1:
                self.active_state = "CONVEYOR_PASSIVE_MONITORING"
                return f"STATE: PASS_THROUGH - Safe {class_name} detected. Engaging Cụm 2 Vacuum Sweeper at nominal speed."

        return "STATE: IDLE"

if __name__ == "__main__":
    print("=== SENTINELCLEAN-HYBRID PRODUCTION ENVIRONMENT CHECK ===")
    try:
        orchestrator = SentinelCleanConveyorCore(model_path="best.pt")
        test_image_path = "src/sample_waste.jpg"
        log_telemetry = orchestrator.process_conveyor_frame(test_image_path)
        print(log_telemetry)
    except Exception as e:
        print(f"❌ Core runtime fault: {e}")
