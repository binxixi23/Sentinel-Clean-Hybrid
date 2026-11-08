import cv2
import os
import numpy as np

def create_before_after_view():
    print("=== SENTINELCLEAN-HYBRID COMPARISON GENERATOR ===")
    
    original_path = "src/sample_waste.jpg"
    annotated_path = "results/inference_output/result_spill.jpg" # Khớp chính xác với tên file của cụm code mới
    output_dir = "results/inference_output"
    output_path = os.path.join(output_dir, "before_after_comparison.jpg")
    
    if not os.path.exists(original_path) or not os.path.exists(annotated_path):
        print("❌ Error: Missing required original input or result_spill.jpg image.")
        print("👉 Action Required: Run 'python demo_spill.py' first to generate the result image.")
        return
        
    img_before = cv2.imread(original_path)
    img_after = cv2.imread(annotated_path)
    
    h, w, _ = img_before.shape
    img_after_resized = cv2.resize(img_after, (w, h))
    
    # Chèn biểu ngữ nhãn chữ kiểm thử lên ảnh
    cv2.putText(img_before, "BEFORE (Original Data)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(img_after_resized, "AFTER (YOLOv26 Core)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3, cv2.LINE_AA)
    
    # Ghép hai ma trận ảnh theo chiều ngang song song
    comparison_matrix = np.hstack((img_before, img_after_resized))
    
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(output_path, comparison_matrix)
    
    print(f"🎉 EXPORT SUCCESS: Professional side-by-side image saved to: {output_path}")
    print("=========================================================")

if __name__ == "__main__":
    create_before_after_view()
