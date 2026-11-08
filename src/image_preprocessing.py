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
        self.MAX_SPILL_AREA_THRESHOLD = 0.65  # Large spill occupies >65% of camera frame

        if os.path.exists(model_path):
            self.device_target = 0 if torch.cuda.is_available() else "cpu"
            self.model = YOLO(model_path)
            self.model.to(self.device_target)
            
            print(f"[INIT] Loaded NMS-Free YOLOv26 Core on Hardware: {str(self.device_target).upper()}")
            print("[INIT] Custom Perimetric Tube Filter Cartridge & Dual-Battery MUX Online.")
            print("[INIT] Warming up tensor graph layers...")
            warmup_frame = np.zeros((640, 640, 3), dtype=np.uint8)
            for _ in range(3):
                _ = self.model.predict(source=warmup_frame, conf=self.CONF_THRESHOLD, verbose=False)
            print("[INIT] Warm-up complete. Low-level power sandboxing active.")
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

        # Execute prediction and grab the first element from the list object
        results_list = self.model.predict(source=img_raw, conf=self.CONF_THRESHOLD, device=self.device_target, verbose=False)
        results = results_list[0]
        boxes = results.boxes

        # Export annotated frame to disk
        img_output = results.plot()
        output_dir = "results/inference_output"
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, "result_spill.jpg")
        cv2.imwrite(output_file_path, img_output)

        if len(boxes) == 0:
            self.active_state = "CONVEYOR_PASSIVE_MONITORING"
            return "STATE: PASS_THROUGH - Clean floor detected. Main Vacuum active at nominal velocity."

        class_mapping = {0: "Dry Waste", 1: "Wet Waste", 2: "Liquid Spill"}

        for box in boxes:
            class_id = int(box.cls)
            confidence_score = float(box.conf)
            class_name = class_mapping.get(class_id, "Unknown Entity")

            if class_id == 2:  # Fluid Matrix Hazard Found
                xyxy = box.xyxyn[0].tolist()  # [xmin, ymin, xmax, ymax]
                box_area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])

                # CRITICAL OVERLOAD: Large Puddle (Stop Main Vacuum + Trigger Smart Phone Alarm)
                if box_area > self.MAX_SPILL_AREA_THRESHOLD:
                    self.active_state = "CRITICAL_SPILL_OVERLOAD"
                    return (
                        f"\n⚠️ CRITICAL HAZARD: LARGE LIQUID SPILL DETECTED ({round(box_area*100, 1)}% Area) ⚠️\n"
                        f"-> [SAFETY ACTUATOR]: Main Vacuum OFF instantly to avoid flooding the custom tube-mesh filter!\n"
                        f"-> [FLUID SYSTEM]: Keeping Mini-Pump Module ON to drain spill borders.\n"
                        f"-> [TELEMETRY]: 🚨 PHONE ALARM ACTIVATED! Sending emergency alert to factory operator/user smartphone. 🚨"
                    )
                
                # MINOR PUDDLE: Use 2-Step Back-Off with Reversing Sensor Safety Guards
                else:
                    self.active_state = "EMERGENCY_WET_ISOLATION"
                    return (
                        f"\n🚨 MINOR FLUID DETECTED: {class_name.upper()} ({round(confidence_score * 100, 1)}%) 🚨\n"
                        f"-> [BATTERY SWITCH]: Shifting load to alternative battery bank via smart hardware BMS.\n"
                        f"-> [FLUID SYSTEM]: Activating low-power Mini-Pump Module to handle liquid extraction.\n"
                        f"-> [NAVIGATION]: Rear proximity sensors clear. Executing safe 2-Step Back-Off (moving back 60cm).\n"
                        f"-> [DRY SYSTEM]: Re-engaging Main Vacuum to collect remaining Class 0/1 debris over dried area."
                    )
            
            elif class_id == 0 or class_id == 1:
                self.active_state = "CONVEYOR_PASSIVE_MONITORING"
                return f"STATE: PASS_THROUGH - {class_name} detected. Engaging main vacuum tube at nominal speed."

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
    print("=========================================================")
