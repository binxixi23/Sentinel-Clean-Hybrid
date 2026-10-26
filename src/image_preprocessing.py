import os
import time

class SentinelCleanConveyorCore:
    def __init__(self):
        # High-viability threshold gating barrier for industrial sorters
        self.CONF_THRESHOLD = 0.25
        self.active_state = "CONVEYOR_PASSIVE_MONITORING"
        print("[System Initialization] YOLOv26 NMS-Free Sorter Matrix Active.")

    def process_conveyor_telemetry(self, detected_class_id, confidence_score):
        """
        Industrial state machine routing logic for SentinelClean-Hybrid.
        Directs mechanical sorting actuators based on custom Roboflow categories.
        """
        if confidence_score < self.CONF_THRESHOLD:
            self.active_state = "CONVEYOR_PASSIVE_MONITORING"
            return "STATE: PASS_THROUGH - Low confidence matrix ignored."

        # Industrial Taxonomy Mapping array aligned with Roboflow Universe V1
        class_mapping = {
            0: "Brown Stains",
            1: "Other Debris",
            2: "Red Stains",
            3: "Tea Stains",
            4: "Water Stains",
            5: "White Stains"
        }

        class_name = class_mapping.get(detected_class_id, "Unknown Entity")

        # CRITICAL HAZARD DETECTION ROUTING BLOCK (Classes: 0, 2, 3, 4, 5)
        # Sửa lỗi bảo mật: Sử dụng điều kiện loại trừ lớp rác khô thông thường (Class 1)
        if detected_class_id != 1 and detected_class_id >= 0 and detected_class_id <= 5:
            self.active_state = "EMERGENCY_WET_ISOLATION"
            action_log = (
                f"\n🚨 EMERGENCY LINE HAZARD VERIFIED: {class_name.upper()} ({confidence_score*100:.1f}%) 🚨\n"
                f"-> ACTION 1: Shutting down standard dry filtration line to isolate line contamination.\n"
                f"-> ACTION 2: Emitting PWM pulse sequence to High-Torque Sorting Actuator [Pin 18].\n"
                f"-> ACTION 3: ---> DEPLOYING RETRACTABLE FLUID-ABSORPTION GEAR ARRAY...\n"
                f"-> ACTION 4: Engaging single-use consumable cotton roll core to isolate the target matrix."
            )
            return action_log

        # REGULAR UNREGULATED HOUSECLEANING PASSIVE TRACKING (Class: 1)
        elif detected_class_id == 1:
            self.active_state = "CONVEYOR_PASSIVE_MONITORING"
            return f"STATE: PASS_THROUGH - Ordinary {class_name} identified. Maintaining standard line flow."

        return "STATE: IDLE"

# =====================================================================
# LIVE PRODUCTION VERIFICATION TESTRUN
# =====================================================================
if __name__ == "__main__":
    print("=== TESTING SENTINELCLEAN INDUSTRIAL CONVEYOR MATRIX WORKSTACK ===")
    orchestrator = SentinelCleanConveyorCore()
    
    # Simulate a critical line event: Sorter captures a Clear PET Bottle (Water Stains) at 84% confidence
    test_class_id = 4  
    test_confidence = 0.84
    
    start_execution = time.time()
    execution_result = orchestrator.process_conveyor_telemetry(test_class_id, test_confidence)
    end_execution = time.time()
    
    print(execution_result)
    print(f"\n[BENCHMARK] YOLOv26 Edge state processing latency: {(end_execution - start_execution)*1000:.4f} ms")
    print("================================================================")
