import os
import pandas as pd
import matplotlib.pyplot as plt

def build_production_performance_charts(csv_path="results/results.csv", output_dir="results"):
    print("=== SENTINELCLEAN-HYBRID DATA VISUALIZATION ENGINE ===")
    
    if not os.path.exists(csv_path):
        print(f"❌ File system exception: Matrix table not found at path '{csv_path}'.")
        print("👉 Action Required: Verify your 'results.csv' file remains inside your local 'results/' folder.")
        return

    # Ingest training log data matrices
    try:
        df = pd.read_csv(csv_path)
        # Strip trailing or hidden whitespace structures from headers
        df.columns = df.columns.str.strip()
        
        # Verify required headers exist
        required_columns = ['epoch', 'train/box_loss', 'train/cls_loss', 'metrics/mAP50(B)']
        for col in required_columns:
            if col not in df.columns:
                # Attempt structural fallback fallback matching for different ultralytics revisions
                alt_col = col.replace('(B)', '')
                if alt_col in df.columns:
                    df.rename(columns={alt_col: col}, inplace=True)
                else:
                    raise KeyError(f"Missing expected metrics header registration: '{col}'")
                    
        print(f"✅ Ingested training record telemetry. Total recorded cycles: {len(df)} epochs.")
    except Exception as e:
        print(f"❌ Data ingestion fault: Unable to parse matrix columns. Error: {e}")
        return

    # Initialize layout dimensions for clean document presentation
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax1 = plt.subplots(figsize=(11, 5.5))

    # --- Plot Line Layer 1: Convergence Loss Curves (Left Y-Axis) ---
    color_box = '#D32F2F' # Industrial Crimson
    color_cls = '#388E3C' # Deep Emerald
    
    ax1.set_xlabel('Huấn luyện Epoch (Vòng lặp tối ưu)', fontsize=12, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Loss Metrics (Sai số ma trận)', fontsize=12, fontweight='bold', color='#212121')
    
    line1 = ax1.plot(df['epoch'], df['train/box_loss'], color=color_box, linestyle='-', linewidth=2.5, label='Train Box Loss (Sai số khung)')
    line2 = ax1.plot(df['epoch'], df['train/cls_loss'], color=color_cls, linestyle='--', linewidth=2.5, label='Train Cls Loss (Sai số nhãn)')
    ax1.tick_params(axis='y', labelcolor='#212121')
    
    # --- Plot Line Layer 2: Precision Mean Average Precision (Right Y-Axis) ---
    ax2 = ax1.twinx()
    color_map = '#1976D2' # Cobalt Blue
    ax2.set_ylabel('Mean Average Precision (Độ chính xác mAP @0.5)', fontsize=12, fontweight='bold', color=color_map)
    
    line3 = ax2.plot(df['epoch'], df['metrics/mAP50(B)'], color=color_map, linestyle='-', linewidth=3.0, label='mAP @0.5 Accuracy (Độ chính xác)')
    ax2.tick_params(axis='y', labelcolor=color_map)
    ax2.set_ylim(0, 1.05) # Force scale boundaries to reflect true normalized percentage limits

    # Merge legends from dual twin axes arrays into a single presentation grid box
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, facecolor='#FFFFFF', edgecolor='#E0E0E0', fontsize=10)

    plt.title('SENTINELCLEAN-HYBRID: AI TRAINING CORE METRICS (YOLOv26)', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    
    # Commit rendering to disk
    os.makedirs(output_dir, exist_ok=True)
    target_output_path = os.path.join(output_dir, "training_performance_curves.png")
    plt.savefig(target_output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"🎉 SUCCESS: High-impact chart compiled and exported to: {target_output_path}")
    print("👉 Next Action: Open this file on your computer and paste it directly into your report chapters.")
    print("=================================================================")

if __name__ == "__main__":
    build_production_performance_charts()
