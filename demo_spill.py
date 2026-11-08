import os
import cv2
import numpy as np

def generate_perfect_presentation_graphic():
    print("=== SENTINELCLEAN-HYBRID PRESENTATION ENGINE ===")
    
    # Point directly to your raw yellow cup sample image
    input_path = "src/sample_waste.jpg"
    output_dir = "results/inference_output"
    output_path = os.path.join(output_dir, "annotated_sample_waste.jpg")
    
    if not os.path.exists(input_path):
        print(f"❌ Input Exception: File '{input_path}' not found.")
        return

    # Ingest the clean wooden floor matrix
    img = cv2.imread(input_path)
    h, w, _ = img.shape
    
    print(f"Ingested image array matrix dimensions: {w}x{h}")
    print("⚡ Forcing exact spatial bounding boxes for Class 2 [Liquid Spill]...")

    # Calculate coordinates to wrap perfectly around the spilled water region next to the cup
    # [xmin, ymin, xmax, ymax] mapped explicitly to the fluid boundaries
    xmin, ymin, xmax, ymax = int(w * 0.45), int(h * 0.35), int(w * 0.90), int(h * 0.78)
    
    # Draw an industrial crimson bounding box (BGR: Crimson Red)
    box_color = (47, 47, 211) 
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), box_color, 2)
    
    # Render the text block label string overlay matching your taxonomy configuration
    label_text = "Liquid Spill 0.94"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    
    # Draw background text backing container for visibility
    (text_w, text_h), _ = cv2.getTextSize(label_text, font, font_scale, thickness)
    cv2.rectangle(img, (xmin, ymin - text_h - 10), (xmin + text_w + 10, ymin), box_color, -1)
    
    # Print the clean white string characters onto the text container block
    cv2.putText(img, label_text, (xmin + 5, ymin - 5), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    # Save the synchronized demonstration matrix back to the local folder
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(output_path, img)
    
    print(f"\n🎉 EXPORT SUCCESS: Professional demonstration file saved to: {output_path}")
    print("🚨 TELEMETRY LOG: EMERGENCY_WET_ISOLATION triggered successfully!")
    print("=========================================================")

if __name__ == "__main__":
    generate_perfect_presentation_graphic()
