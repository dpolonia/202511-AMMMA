"""
Configuration file for paper analysis workflow.
Loads API keys and defines search parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR
ARCHIVE_DIR = BASE_DIR / "Docs" / "archive"

# Determine Output Directory (Run Folder)
# If AMMMA_RUN_DIR env var is set, use it. Otherwise, use BASE_DIR.
if os.getenv("AMMMA_RUN_DIR"):
    OUTPUT_DIR = Path(os.getenv("AMMMA_RUN_DIR"))
else:
    OUTPUT_DIR = BASE_DIR

SELECTED_PAPER_DIR = OUTPUT_DIR / "selected_paper"

# Ensure directories exist
if not os.getenv("AMMMA_RUN_DIR"):
    # Only create if we are NOT in a run (scripts creating their own dirs)
    # If we are in a run, main.py handles creation
    SELECTED_PAPER_DIR.mkdir(exist_ok=True)

# API Keys
SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Scopus API Configuration
SCOPUS_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"
SCOPUS_SERIAL_URL = "https://api.elsevier.com/content/serial/title"

# Search Parameters
SEARCH_KEYWORDS = {
    "fundamental": {
        "multilevel": ["multilevel", "multi-level", "hierarchical linear model", "HLM", "nested data", "hierarchical model"],
        "mixed_methods": ["mixed method", "mixed-method", "qualitative and quantitative", "multi-method"]
    },
    "nice_to_have": {
        "vbhc": ["value-based healthcare", "VBHC", "value based care", "value-based care"],
        "context": ["national health service", "NHS", "Beveridge", "Portugal", "Portuguese"],
    }
}

# Grading Weights (Total: 100 points)
# User can customize these weights interactively
GRADING_WEIGHTS = {
    "class_relevance": {
        "multilevel_strong": 20,  # Strong multilevel keywords
        "multilevel_weak": 10,    # Weak multilevel keywords
        "mixed_methods_explicit": 15,  # Explicit mixed methods
        "mixed_methods_implicit": 5,   # Implicit mixed methods
    },
    "phd_relevance": {
        "vbhc": 10,              # VBHC keywords
        "nhs_context": 10,       # NHS/Beveridgean context
        "portugal": 5,           # Portugal-specific
    },
    "journal_quality": {
        "citescore_max": 12,     # CiteScore (normalized)
        "sjr_max": 8,            # SJR (normalized)
    },
    "impact": {
        "citations_max": 5,      # Citations (normalized)
    }
}

# LLM Model Options
LLM_MODELS = {
    "anthropic": {
        "opus_4.1": "claude-opus-4.1",
        "sonnet_4.5": "claude-sonnet-4.5",
        "haiku_4.5": "claude-haiku-4.5",
    },
    "openai": {
        "gpt_5.1": "gpt-5.1",
        "gpt_5_mini": "gpt-5-mini",
        "gpt_5_nano": "gpt-5-nano",
        "gpt_4.1": "gpt-4.1",
        "o1": "o1",
        "o1_mini": "o1-mini",
    },
    "google": {
        "gemini_3_pro": "gemini-3-pro-preview",
        "gemini_2.5_pro": "gemini-2.5-pro",
        "gemini_2.5_flash": "gemini-2.5-flash",
        "gemini_2.5_flash_lite": "gemini-2.5-flash-lite",
    },
    "xai": {
        "grok_4.1": "grok-4.1",
        "grok_4.1_fast": "grok-4.1-fast",
        "grok_4": "grok-4",
    }
}

# File paths
PDF_FILES = {
    "class_content": DOCS_DIR / "20241212 SCEE I - AMMMMA.pdf",
    "evaluation_guide": DOCS_DIR / "MMMAME_EvaluationGuideAndChecklist_2025.pdf",
}

# Output files
OUTPUT_FILES = {
    "llm_config": OUTPUT_DIR / "llm_config.json",
    "scopus_results": OUTPUT_DIR / "scopus_results.json",
    "graded_papers": OUTPUT_DIR / "graded_papers.json",
    "top_20_papers": OUTPUT_DIR / "top_20_papers.md",
    "evaluation_draft": OUTPUT_DIR / "evaluation_draft.md",
    "evaluation_final": OUTPUT_DIR / "evaluation_final.md",
    "final_report": OUTPUT_DIR / "final_report.md",
    "presentation": OUTPUT_DIR / "presentation.md",
}
