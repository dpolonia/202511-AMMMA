"""
Main Orchestrator Script
Runs all phases of the paper analysis workflow sequentially.
"""

import sys
from pathlib import Path

import sys
import os
from pathlib import Path
from datetime import datetime

# Import config first to get base paths, but we'll reload it or set env var before other imports if needed
# Actually, we need to set env var BEFORE importing config if we want it to pick it up at module level.
# But config is already imported. We might need to reload it or just rely on the fact that 
# scripts import config when they run.
# Since we are running scripts via __import__, they will share the already imported config module.
# So we need to reload config or modify it directly.

# Better approach: Set env var, then import config.
# If config is already imported by main, we need to reload it.
import importlib

def setup_run_environment():
    """Create run folder and set environment variable."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = Path(__file__).parent
    run_dir = base_dir / f"run_{timestamp}"
    run_dir.mkdir(exist_ok=True)
    
    # Set environment variable
    os.environ["AMMMA_RUN_DIR"] = str(run_dir)
    
    # Reload config to pick up the new path
    if 'config' in sys.modules:
        importlib.reload(sys.modules['config'])
    else:
        import config
        
    return run_dir

# Now import config after setup (or it will be reloaded)
import config

def print_header(phase_name: str):
    """Print phase header."""
    print("\n" + "="*70)
    print(f"  {phase_name}")
    print("="*70)

def run_phase(phase_num: str, phase_name: str, module_name: str) -> bool:
    """
    Run a single phase.
    
    Args:
        phase_num: Phase number (e.g., "0", "1", "4.5")
        phase_name: Human-readable phase name
        module_name: Python module name to import
        
    Returns:
        True if phase completed successfully
    """
    print_header(f"PHASE {phase_num}: {phase_name}")
    
    try:
        # Dynamically import and run the phase module
        module = __import__(module_name)
        result = module.main()
        
        if result:
            print(f"\n✓ Phase {phase_num} completed successfully")
            return True
        else:
            print(f"\n✗ Phase {phase_num} failed")
            return False
    except Exception as e:
        print(f"\n✗ Error in Phase {phase_num}: {e}")
        return False

def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("  PAPER ANALYSIS WORKFLOW - FULL EXECUTION")
    print("="*70)
    
    proceed = input("\nProceed with full workflow? (y/n): ").lower().strip()
    if proceed != 'y':
        print("Workflow cancelled.")
        return

    # Setup run environment
    run_dir = setup_run_environment()
    print(f"\n📂 Created Run Folder: {run_dir.name}")
    print(f"   All outputs will be saved to this directory.")

    print("\nThis script will run all phases of the workflow:")
    print("  Phase 0: LLM Configuration")
    print("  Phase 1: Search Strategy & Data Retrieval")
    print("  Phase 2: Grading Algorithm")
    print("  Phase 3: Paper Selection & Retrieval")
    print("  Phase 4: Evaluation Question Answering")
    print("  Phase 4.5: Adversarial Review & Refinement")
    print("  Phase 5: Final Report Generation")
    print("  Phase 6: Presentation Creation")
    
    # Phase 0: LLM Configuration
    if not run_phase("0", "LLM Configuration", "00_setup_llms"):
        print("\n❌ Workflow stopped at Phase 0")
        return
    
    # Phase 1: Search Strategy
    if not run_phase("1", "Search Strategy & Data Retrieval", "01_search_strategy"):
        print("\n❌ Workflow stopped at Phase 1")
        return
    
    # Phase 2: Grading Algorithm
    if not run_phase("2", "Grading Algorithm", "02_grading_algorithm"):
        print("\n❌ Workflow stopped at Phase 2")
        return
    
    # Phase 3: Paper Retrieval
    if not run_phase("3", "Paper Selection & Retrieval", "03_paper_retrieval"):
        print("\n❌ Workflow stopped at Phase 3")
        return
    
    # Phase 4: Evaluation Answering
    if not run_phase("4", "Evaluation Question Answering", "04_answer_evaluation"):
        print("\n❌ Workflow stopped at Phase 4")
        return
    
    # Phase 4.5: Adversarial Review
    if not run_phase("4.5", "Adversarial Review & Refinement", "04.5_adversarial_review"):
        print("\n❌ Workflow stopped at Phase 4.5")
        return
    
    # Phase 5: Final Report
    if not run_phase("5", "Final Report Generation", "05_generate_report"):
        print("\n❌ Workflow stopped at Phase 5")
        return
    
    # Phase 6: Presentation
    if not run_phase("6", "Presentation Creation", "06_create_presentation"):
        print("\n❌ Workflow stopped at Phase 6")
        return
    
    # Success!
    print("\n" + "="*70)
    print("  ✓ WORKFLOW COMPLETE!")
    print("="*70)
    print("\nAll phases completed successfully!")
    print("\nGenerated files:")
    print(f"  - {config.OUTPUT_FILES['llm_config']}")
    print(f"  - {config.OUTPUT_FILES['scopus_results']}")
    print(f"  - {config.OUTPUT_FILES['graded_papers']}")
    print(f"  - {config.OUTPUT_FILES['top_20_papers']}")
    print(f"  - {config.SELECTED_PAPER_DIR}/")
    print(f"  - {config.OUTPUT_FILES['evaluation_draft']}")
    print(f"  - {config.OUTPUT_FILES['evaluation_final']}")
    print(f"  - {config.OUTPUT_FILES['final_report']}")
    print(f"  - {config.OUTPUT_FILES['presentation']}")
    print("\nYou can now review the final report and presentation!")

if __name__ == "__main__":
    main()
