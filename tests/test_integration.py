# tests/test_integration.py
import io
import pytest
import cv2
import numpy as np
from fastapi.testclient import TestClient

# Khớp chính xác cấu trúc thư mục local
from app.main.app import app

client = TestClient(app)

def create_dummy_stream_buffer():
    """Generates a clean valid encoded image byte stream directly inside memory registers."""
    dummy_matrix = np.zeros((640, 640, 3), dtype=np.uint8)
    cv2.circle(dummy_matrix, (320, 320), 100, (255, 120, 50), -1)
    _, encoded_buffer = cv2.imencode(".jpg", dummy_matrix)
    return io.BytesIO(encoded_buffer.tobytes())

def test_nominal_speed_budget_and_actuation():
    """Validates that real-world processing loop latency stays below the 45.00 ms boundary."""
    stream_file = create_dummy_stream_buffer()
    
    response = client.post(
        "/api/v1/sortation/telemetry",
        files={"file": ("frame.jpg", stream_file, "image/jpeg")}
    )
    
    assert response.status_code == 200
    telemetry = response.json()
    
    assert telemetry["total_latency_ms"] < 45.00, f"Latency threshold broken: {telemetry['total_latency_ms']} ms"
    
    for detection in telemetry["detections"]:
        if detection["class_id"] == 2:  # Liquid Spill Found
            assert telemetry["vacuum_motor_status"] == "SHUTDOWN_WET_PROTECTION"
            assert telemetry["mechanical_pad_roll"] == "DEPLOYED"

def test_conveyor_overload_plan_b_activation():
    """Fires a continuous sequence of frame buffers to forcefully trigger Plan B behaviors."""
    final_mode = "NOMINAL"
    
    for i in range(10):
        stream_file = create_dummy_stream_buffer()
        response = client.post(
            "/api/v1/sortation/telemetry",
            files={"file": ("frame.jpg", stream_file, "image/jpeg")}
        )
        assert response.status_code == 200
        telemetry = response.json()
        final_mode = telemetry["active_mode"]
        
    assert final_mode in ["PLAN_B_SURGE_PROCESSING", "PLAN_B_SKIPPED"]
