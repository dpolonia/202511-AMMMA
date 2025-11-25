"""
Demo Runner Script
Runs the full workflow in automated demo mode using a specific PDF.
"""

import os
import json
import subprocess
import sys

def run_demo():
    # 1. Set Demo PDF Path
    # Handle both Windows and WSL environments
    if os.name == 'nt':
        demo_pdf_path = r"C:\TMP\s41586-023-05772-8.pdf"
    else:
        demo_pdf_path = "/mnt/c/TMP/s41586-023-05772-8.pdf"
    
    os.environ["AMMMA_DEMO_PDF_PATH"] = demo_pdf_path
    
    # 2. Define Automated Inputs
    # Sequence:
    # 1. main.py: "y" (Proceed)
    # 2. Phase 0: "3" (Google for Dev)
    # 3. Phase 0: "4" (Flash Lite for Dev)
    # 4. Phase 0: "3" (Google for DA)
    # 5. Phase 0: "4" (Flash Lite for DA)
    # 6. Phase 2: "n" (Customize weights? No)
    # 7. Phase 3: "1" (Select paper #1)
    # 8. Phase 4.5: "n" (Add comments? No)
    # 9. Phase 4.5: "n" (Continue? No - Finalize)
    
    inputs = ["y", "3", "4", "3", "4", "n", "1", "n", "n"]
    os.environ["AMMMA_DEMO_INPUTS"] = json.dumps(inputs)
    
    print("="*60)
    print("STARTING AUTOMATED DEMO")
    print("="*60)
    print(f"Target PDF: {demo_pdf_path}")
    print(f"Automated Inputs: {inputs}")
    print("-" * 60)
    
    # 3. Run Main Script
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Demo failed with exit code {e.returncode}")
    except KeyboardInterrupt:
        print("\n⚠ Demo interrupted")

if __name__ == "__main__":
    run_demo()
