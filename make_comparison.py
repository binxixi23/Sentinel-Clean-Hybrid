import cv2
import os
import numpy as np

def create_before_after_view():
    print("=== SENTINELCLEAN-HYBRID COMPARISON GENERATOR ===")
    
    # 1. Map input tracks relative to your exact tree directory
    original_path = "src/sample_waste.jpg"
    annotated_path = "results/inference_output/result_spill.jpg"
    output_dir = "results/inference_output"
    output_path = os.path.join(output_dir, "before_after_comparison.jpg")
    
    if not os.path.exists(original_path) or not os.path.exists(annotated_path):
        print("❌ Error: Missing required original input or annotated results image.")
        return
        
    # 2. Ingest image matrix arrays
    img_before = cv2.imread(original_path)
    img_after = cv2.imread(annotated_path)
    
    # Force identical resolution dimensions to prevent spatial mismatch during stitching
    h, w, _ = img_before.shape
    img_after_resized = cv2.resize(img_after, (w, h))
    
    # 3. Inject high-visibility text banners across array layers
    cv2.putText(img_before, "BEFORE (Original)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(img_after_resized, "AFTER (YOLOv26 Core)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3, cv2.LINE_AA)
    
    # 4. Concatenate matrices horizontally side-by-side
    comparison_matrix = np.hstack((img_before, img_after_resized))
    
    # 5. Commit structured output matrix to local storage block
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(output_path, comparison_matrix)
    
    print(f"🎉 EXPORT SUCCESS: Professional side-by-side image saved to: {output_path}")
    print("👉 Next Action: Pull this image file straight into your report figures context.")
    print("=========================================================")

if __name__ == "__main__":
    create_before_after_view()
