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

        # Verify and load your production-trained weights file
        if os.path.exists(model_path):
            self.device_target = 0 if torch.cuda.is_available() else "cpu"
            self.model = YOLO(model_path)
            self.model.to(self.device_target)

            device_label = "GPU (CUDA:0)" if self.device_target == 0 else "CPU"
            print(f"[INIT] Loaded optimized weights checkpoint on: {device_label}")
            print("[INIT] Warming up tensor graph layers...")
            
            warmup_frame = np.zeros((640, 640, 3), dtype=np.uint8)
            for _ in range(3):
                _ = self.model.predict(source=warmup_frame, conf=self.CONF_THRESHOLD, verbose=False)
            print("[INIT] Warm-up complete. Memory registries primed.")
        else:
            raise FileNotFoundError(f"Weight asset '{model_path}' not found at root directory.")

    def process_conveyor_frame(self, image_path):
        """
        Evaluates the local frame matrix, executes YOLO prediction models,
        saves output graphics, and returns system control logic states.
        """
        if not os.path.exists(image_path):
            return "❌ Workspace Exception: Target file is unreachable."

        img_raw = cv2.imread(image_path)
        if img_raw is None:
            return "❌ Matrix Parsing Error: Image array stream is empty or unreadable."

        if np.max(img_raw) == np.min(img_raw):
            return "❌ Input Constraint Violation: Image is fully blank or black. Please replace src/sample_waste.jpg with a real picture file."

        # Execute active graph prediction model layers directly on native format
        results = self.model.predict(source=img_raw, conf=self.CONF_THRESHOLD, device=self.device_target, verbose=False)[0]
        boxes = results.boxes

        # Draw bounding boxes and text overlays onto the output array matrix
        img_output = results.plot()

        output_dir = "results/inference_output"
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, "annotated_sample_waste.jpg")

        # Commit updated validation visual files onto local disk storage structures
        cv2.imwrite(output_file_path, img_output)
        print(f"[SYSTEM] Annotated validation matrix exported to: {output_file_path}")

        if len(boxes) == 0:
            self.active_state = "CONVEYOR_PASSIVE_MONITORING"
            return "STATE: PASS_THROUGH - Clean line telemetry. Maintaining nominal conveyor velocity."

        # Unified 3-Class Production Taxonomy Map
        class_mapping = {0: "Dry Waste", 1: "Wet Waste", 2: "Liquid Spill"}

        for box in boxes:
            class_id = int(box.cls[0])
            confidence_score = float(box.conf[0])
            class_name = class_mapping.get(class_id, "Unknown Entity")

            # Active state machine routing for wet/fluid cross-contamination anomalies
            if class_id == 1 or class_id == 2:
                self.active_state = "EMERGENCY_WET_ISOLATION"
                return (
                    f"\n🚨 INDUSTRIAL HAZARD FLAGGED: {class_name.upper()} ({round(confidence_score * 100, 1)}%) 🚨\n"
                    f"-> ACTION 1: Disrupting nominal line progression to isolate material cross-contamination.\n"
                    f"-> ACTION 2: Injecting high-torque PWM actuator actuation protocols onto micro-pin 18.\n"
                    f"-> ACTION 3: DEPLOYING RETRACTABLE WATER-ABSORPTION RECOVERY MECHANISMS UNTO CONVEYOR SURFACE...\n"
                    f"-> ACTION 4: Engaging single-use consumable high-absorption filtration core asset (Razor & Blades Model)."
                )
            elif class_id == 0:
                self.active_state = "CONVEYOR_PASSIVE_MONITORING"
                return f"STATE: PASS_THROUGH - Safe {class_name} detected. Maintaining nominal conveyor velocity."

        return "STATE: IDLE"
if __name__ == "__main__":
    print("=== SENTINELCLEAN-HYBRID PRODUCTION ENVIRONMENT CHECK ===")
    try:
        orchestrator = SentinelCleanConveyorCore(model_path="best.pt")
        test_image_path = "src/sample_waste.jpg"

        # -----------------------------------------------------------------
        # TẠM THỜI TẮT ĐOẠN TỰ SINH ẢNH GIẢ LẬP ĐỂ CHẠY ẢNH CỐC NƯỚC ĐỔ THỰC TẾ
        # -----------------------------------------------------------------
        # os.makedirs("src", exist_ok=True)
        # fake_image = np.ones((640, 640, 3), dtype=np.uint8) * 255
        # fake_image[:, :, 0] = 255  
        # fake_image[:, :, 1] = 120  
        # fake_image[:, :, 2] = 50   
        # cv2.circle(fake_image, (320, 320), 150, (0, 0, 255), -1) 
        # cv2.imwrite(test_image_path, fake_image)
        # -----------------------------------------------------------------

        print(f"\n--- Simulating real-time webcam/sensor stream frame pass: {test_image_path} ---")
        start_time = time.time()
        log_telemetry = orchestrator.process_conveyor_frame(test_image_path)
        end_time = time.time()

        print(log_telemetry)
        print(f"\n[BENCHMARK] Active control logic processing latency: {round((end_time - start_time) * 1000, 4)} ms")
    except Exception as e:
        print(f"❌ Core runtime initialization fault: {e}")
    print("=========================================================")

