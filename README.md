# Paper Analysis Workflow

Automated end-to-end workflow for selecting and analyzing academic papers for the **Multilevel and Mixed Methods Approaches** class.

## Overview

This workflow automates the process of:
1. Searching Scopus for relevant papers
2. Grading papers based on class requirements
3. Retrieving and analyzing the selected paper
4. Generating evaluation answers with adversarial review
5. Creating final deliverables (report + presentation)

## Prerequisites

### Required API Keys

Add the following to your `.env` file:

```bash
SCOPUS_API_KEY=your_scopus_key
ANTHROPIC_API_KEY=your_anthropic_key  # Optional
OPENAI_API_KEY=your_openai_key        # Optional
GOOGLE_API_KEY=your_google_key        # Optional
XAI_API_KEY=your_xai_key              # Optional
```

**Note**: You need at least ONE LLM API key (Anthropic, OpenAI, Google, or xAI) for Phases 4-6.

### Required Software

- Python 3.8+
- `pdftotext` (for PDF text extraction)
  - Ubuntu/WSL: `sudo apt-get install poppler-utils`
  - macOS: `brew install poppler`
  - Windows: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)

### Python Dependencies

```bash
pip install requests python-dotenv
```

## Quick Start

### Option 1: Run Full Workflow

```bash
python main.py
```

This runs all phases sequentially with interactive prompts.

### Option 2: Run Individual Phases

```bash
# Phase 0: Select LLMs
python 00_setup_llms.py

# Phase 1: Search Scopus
python 01_search_strategy.py

# Phase 2: Grade papers (customize weights)
python 02_grading_algorithm.py

# Phase 3: Select and download paper
python 03_paper_retrieval.py

# Phase 4: Generate evaluation answers
python 04_answer_evaluation.py

# Phase 4.5: Adversarial review (2 iterations)
python 04.5_adversarial_review.py

# Phase 5: Generate final report
python 05_generate_report.py

# Phase 6: Create presentation
python 06_create_presentation.py
```

## Workflow Details

### Phase 0: LLM Configuration

**Purpose**: Select AI models for analysis

**Features**:
- Detects available API keys
- Interactive selection of Development and Devil's Advocate LLMs
- Supports 4 providers: Anthropic, OpenAI, Google, xAI
- Validates API connectivity

**Output**: `llm_config.json`

---

### Phase 1: Search Strategy

**Purpose**: Search Scopus for relevant papers

**Search Criteria**:
- **Fundamental** (required): Multilevel + Mixed Methods
- **Nice-to-have**: VBHC + NHS/Beveridgean + Portugal

**Features**:
- Fallback to relaxed search if <20 results
- Retrieves up to 200 papers

**Output**: `scopus_results.json`

---

### Phase 2: Grading Algorithm

**Purpose**: Score and rank papers

**Scoring System** (100 points):
- **Class Relevance** (50 pts): Multilevel + Mixed Methods
- **PhD Relevance** (25 pts): VBHC + NHS + Portugal
- **Journal Quality** (20 pts): CiteScore + SJR
- **Impact** (5 pts): Citations

**Features**:
- **Interactive weight customization**
- Automatic normalization to 100 points
- Detailed score breakdown

**Output**: `graded_papers.json`, `top_20_papers.md`

---

### Phase 3: Paper Retrieval

**Purpose**: Download selected paper and related papers

**Download Methods**:
1. Scopus API
2. DOI resolution
3. Unpaywall (Open Access)
4. Manual upload (fallback)

**Features**:
- Downloads **cited papers** (references)
- Downloads **citing papers**
- Extracts text using `pdftotext`

**Output**: 
- `selected_paper/paper.pdf`
- `selected_paper/paper_text.txt`
- `selected_paper/paper_metadata.json`
- `selected_paper/cited_papers/` (up to 10 papers)
- `selected_paper/citing_papers/` (up to 10 papers)
- `selected_paper/related_papers_metadata.json`

---

### Phase 4: Evaluation Answering

**Purpose**: Generate initial answers to evaluation questions

**Process**:
- Development LLM analyzes paper
- Answers 12 evaluation questions
- Assigns confidence scores

**Output**: `evaluation_draft.md`

**Note**: This phase requires LLM API integration. Current implementation includes placeholders for actual API calls.

---

### Phase 4.5: Adversarial Review

**Purpose**: Improve answer quality through critical dialogue

**Process** (2 iterations):

**Iteration 1**:
1. Devil's Advocate LLM critiques draft
2. Development LLM revises answers

**Iteration 2**:
3. Devil's Advocate performs second review
4. Development LLM finalizes answers

**Features**:
- Identifies shortcomings
- Suggests alternative papers if needed

**Output**: 
- `adversarial_critique_round1.md`
- `evaluation_draft_v2.md`
- `adversarial_critique_round2.md`
- `evaluation_final.md`
- `shortcomings_assessment.md`

---

### Phase 5: Final Report

**Purpose**: Create comprehensive deliverable

**Contents**:
- Methodology explanation
- Selected paper summary
- Evaluation answers
- Score breakdown
- GitHub links

**Output**: `final_report.md`

---

### Phase 6: Presentation

**Purpose**: Generate 8-slide, 15-minute presentation

**Slide Structure**:
1. Title & Context
2. Research Question & Objectives
3. Multilevel Analysis Approach
4. Mixed Methods Integration
5. Key Findings
6. Implications for VBHC
7. Limitations & Future Research
8. Discussion & Questions

**Output**: `presentation.md`

**Note**: Requires customization with actual paper content.

---

## File Structure

```
202511-AMMMA/
├── .env                          # API keys
├── .git/                         # Git repository
├── config.py                     # Configuration
├── utils.py                      # Utility functions
├── main.py                       # Orchestrator
├── 00_setup_llms.py             # Phase 0
├── 01_search_strategy.py        # Phase 1
├── 02_grading_algorithm.py      # Phase 2
├── 03_paper_retrieval.py        # Phase 3
├── 04_answer_evaluation.py      # Phase 4
├── 04.5_adversarial_review.py   # Phase 4.5
├── 05_generate_report.py        # Phase 5
├── 06_create_presentation.py    # Phase 6
├── README.md                     # This file
├── IMPLEMENTATION_SUMMARY.md     # Implementation overview
├── llm_model_comparison.md       # LLM comparison guide
├── 20241212 SCEE I - AMMMMA.pdf # Class content
├── MMMAME_EvaluationGuideAndChecklist_2025.pdf # Evaluation guide
├── llm_config.json              # Generated: LLM config
├── scopus_results.json          # Generated: Search results
├── graded_papers.json           # Generated: Scored papers
├── top_20_papers.md             # Generated: Top 20 list
├── evaluation_draft.md          # Generated: Initial answers
├── evaluation_final.md          # Generated: Final answers
├── final_report.md              # Generated: Final deliverable
├── presentation.md              # Generated: Presentation
├── Docs/                        # Archive folder
│   └── archive/                 # Previous work files
└── selected_paper/              # Generated: Paper files
    ├── paper.pdf
    ├── paper_text.txt
    ├── paper_metadata.json
    ├── related_papers_metadata.json
    ├── cited_papers/            # Referenced papers
    └── citing_papers/           # Papers citing this one
```

## Customization

### Grading Weights

Phase 2 allows interactive customization of all weights:

```
Class Relevance (50 pts default):
  - Multilevel (strong): 20
  - Multilevel (weak): 10
  - Mixed Methods (explicit): 15
  - Mixed Methods (implicit): 5

PhD Relevance (25 pts default):
  - VBHC: 10
  - NHS Context: 10
  - Portugal: 5

Journal Quality (20 pts default):
  - CiteScore: 12
  - SJR: 8

Impact (5 pts default):
  - Citations: 5
```

Weights are automatically normalized to 100 points.

### Search Keywords

Edit `config.py` to modify search keywords:

```python
SEARCH_KEYWORDS = {
    "fundamental": {
        "multilevel": [...],
        "mixed_methods": [...]
    },
    "nice_to_have": {
        "vbhc": [...],
        "context": [...]
    }
}
```

## LLM Model Options

### Recommended Combinations

**Best Overall (Cost)**: GPT-5 mini + GPT-5 nano ($0.04/paper)

**Best Overall (Quality)**: GPT-5.1 + GPT-5 nano ($0.16/paper)

**Best for Long Papers**: Gemini 2.5 Pro + Gemini 2.5 Flash ($0.16/paper)

See `llm_model_comparison.md` for full comparison.

## Troubleshooting

### Scopus API Issues

If you encounter 401 errors:
1. Verify `SCOPUS_API_KEY` in `.env`
2. Check API key permissions on Elsevier Developer Portal
3. Note: Article-level metrics may require institutional access

### PDF Download Failures

If automatic download fails:
1. The script will prompt for manual upload
2. Download from DOI link or publisher
3. Save as `selected_paper/paper.pdf`

### Text Extraction Issues

If `pdftotext` fails:
1. Verify `poppler-utils` is installed
2. Check PDF is not encrypted/protected
3. Try manual text extraction

## Known Limitations

1. **LLM Integration**: Phases 4-6 contain placeholder code for LLM API calls. Full integration requires implementing actual API calls for your chosen provider.

2. **Scopus API**: Some metrics (e.g., dynamic citation counts) may not be accessible depending on your API key permissions.

3. **PDF Availability**: Not all papers are available for automated download. Manual fallback is provided.

## Contributing

To extend this workflow:

1. **Add new scoring criteria**: Edit `02_grading_algorithm.py`
2. **Add new LLM providers**: Edit `config.py` and `00_setup_llms.py`
3. **Customize evaluation questions**: Edit `04_answer_evaluation.py`

## License

This workflow is for academic use in the Multilevel and Mixed Methods Approaches class.

## Contact

For questions or issues, please contact [your email].
