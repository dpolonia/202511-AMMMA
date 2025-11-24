"""
Phase 5: Final Report Generation
Create comprehensive final deliverable document.
"""

from pathlib import Path
from datetime import datetime
import config
import utils

def load_paper_metadata():
    """Load selected paper metadata."""
    metadata_path = config.SELECTED_PAPER_DIR / "paper_metadata.json"
    try:
        return utils.load_json(metadata_path)
    except FileNotFoundError:
        print("❌ ERROR: paper_metadata.json not found!")
        return None

def load_final_evaluation():
    """Load final evaluation answers."""
    eval_path = config.OUTPUT_FILES['evaluation_final']
    try:
        with open(eval_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("⚠ Warning: evaluation_final.md not found, using draft")
        try:
            eval_path = config.OUTPUT_FILES['evaluation_draft']
            with open(eval_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

def generate_methodology_section() -> str:
    """Generate methodology section explaining the workflow."""
    methodology = """## Methodology

### Overview

This analysis was conducted using a comprehensive, automated workflow designed to identify, evaluate, and analyze academic papers for the Multilevel and Mixed Methods Approaches class.

### Workflow Phases

#### Phase 0: LLM Configuration
- **Purpose**: Select AI models for analysis and critical review
- **Implementation**: [`00_setup_llms.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/00_setup_llms.py)
- **Output**: `llm_config.json` with selected Development and Devil's Advocate LLMs

#### Phase 1: Search Strategy & Data Retrieval
- **Purpose**: Execute Scopus API search for relevant papers
- **Implementation**: [`01_search_strategy.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/01_search_strategy.py)
- **Search Criteria**:
  - **Fundamental** (required): Multilevel analysis + Mixed methods
  - **Nice-to-have**: VBHC + NHS/Beveridgean context + Portugal
- **Fallback Strategy**: Relaxed search if strict criteria yield <20 results
- **Output**: `scopus_results.json`

#### Phase 2: Grading Algorithm
- **Purpose**: Score and rank papers based on multiple criteria
- **Implementation**: [`02_grading_algorithm.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/02_grading_algorithm.py)
- **Scoring System** (100 points total):
  - Class Relevance (50 pts): Multilevel + Mixed Methods keywords
  - PhD Relevance (25 pts): VBHC + NHS context + Portugal
  - Journal Quality (20 pts): CiteScore + SJR
  - Impact (5 pts): Citation count
- **Customization**: Interactive weight adjustment with automatic normalization
- **Output**: `graded_papers.json`, `top_20_papers.md`

#### Phase 3: Paper Selection & Retrieval
- **Purpose**: Download and extract selected paper
- **Implementation**: [`03_paper_retrieval.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/03_paper_retrieval.py)
- **Download Methods**:
  1. Scopus API full-text link
  2. DOI resolution
  3. Unpaywall (Open Access)
  4. Manual upload (fallback)
- **Output**: PDF, extracted text, metadata

#### Phase 4: Evaluation Question Answering
- **Purpose**: Generate initial answers to evaluation checklist
- **Implementation**: [`04_answer_evaluation.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/04_answer_evaluation.py)
- **Process**: Development LLM analyzes paper and answers each question
- **Output**: `evaluation_draft.md` with confidence scores

#### Phase 4.5: Adversarial Review & Refinement
- **Purpose**: Improve answer quality through critical dialogue
- **Implementation**: [`04.5_adversarial_review.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/04.5_adversarial_review.py)
- **Process** (2 iterations):
  - **Iteration 1**: Devil's Advocate critique → Development LLM revision
  - **Iteration 2**: Second critique → Final refinement
- **Output**: `evaluation_final.md`, shortcomings assessment

#### Phase 5: Final Report Generation
- **Purpose**: Create comprehensive deliverable document
- **Implementation**: [`05_generate_report.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/05_generate_report.py)
- **Output**: This document

#### Phase 6: Presentation Creation
- **Purpose**: Generate 8-slide, 15-minute presentation
- **Implementation**: [`06_create_presentation.py`](file:///wsl.localhost/Ubuntu/home/dpolonia/202511-AMMMA/Docs/06_create_presentation.py)
- **Output**: `presentation.md`

### Rationale

This workflow ensures:
1. **Transparency**: All steps documented and reproducible
2. **Objectivity**: Quantitative scoring with customizable weights
3. **Quality**: Multi-LLM adversarial review process
4. **Efficiency**: Automated search, retrieval, and analysis
5. **Rigor**: Systematic evaluation against class criteria
"""
    return methodology

def generate_paper_summary(paper_metadata) -> str:
    """Generate summary of selected paper."""
    grading = paper_metadata.get('grading', {})
    breakdown = grading.get('breakdown', {})
    
    summary = f"""## Selected Paper

### Citation

**Title**: {paper_metadata.get('title', 'N/A')}

**Authors**: {paper_metadata.get('authors', 'N/A')}

**Journal**: {paper_metadata.get('publication_name', 'N/A')}

**Year**: {paper_metadata.get('cover_date', 'N/A')[:4] if paper_metadata.get('cover_date') != 'N/A' else 'N/A'}

**DOI**: [{paper_metadata.get('doi', 'N/A')}](https://doi.org/{paper_metadata.get('doi', '')})

**Citations**: {paper_metadata.get('cited_by_count', 0)}

### Selection Rationale

**Total Score**: {grading.get('total_score', 0)}/100

**Score Breakdown**:
- **Class Relevance** ({breakdown.get('class_relevance', {}).get('subtotal', 0)}/50):
  - Multilevel (strong): {breakdown.get('class_relevance', {}).get('multilevel_strong', 0)}/20
  - Multilevel (weak): {breakdown.get('class_relevance', {}).get('multilevel_weak', 0)}/10
  - Mixed Methods (explicit): {breakdown.get('class_relevance', {}).get('mixed_methods_explicit', 0)}/15
  - Mixed Methods (implicit): {breakdown.get('class_relevance', {}).get('mixed_methods_implicit', 0)}/5

- **PhD Relevance** ({breakdown.get('phd_relevance', {}).get('subtotal', 0)}/25):
  - VBHC: {breakdown.get('phd_relevance', {}).get('vbhc', 0)}/10
  - NHS Context: {breakdown.get('phd_relevance', {}).get('nhs_context', 0)}/10
  - Portugal: {breakdown.get('phd_relevance', {}).get('portugal', 0)}/5

- **Journal Quality** ({breakdown.get('journal_quality', {}).get('subtotal', 0)}/20):
  - CiteScore: {breakdown.get('journal_quality', {}).get('citescore', 0)}/12 (raw: {breakdown.get('journal_quality', {}).get('raw_citescore', 'N/A')})
  - SJR: {breakdown.get('journal_quality', {}).get('sjr', 0)}/8 (raw: {breakdown.get('journal_quality', {}).get('raw_sjr', 'N/A')})

- **Impact** ({breakdown.get('impact', {}).get('subtotal', 0)}/5):
  - Citations: {breakdown.get('impact', {}).get('citations', 0)}/5 (raw: {breakdown.get('impact', {}).get('raw_citations', 0)})

### Abstract

{paper_metadata.get('abstract', 'N/A')}
"""
    return summary

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 5: FINAL REPORT GENERATION")
    print("="*60)
    
    # Load paper metadata
    paper_metadata = load_paper_metadata()
    if not paper_metadata:
        print("❌ Cannot generate report without paper metadata")
        return False
    
    # Load final evaluation
    evaluation = load_final_evaluation()
    if not evaluation:
        print("⚠ Warning: No evaluation found, report will be incomplete")
    
    # Generate report
    print("\nGenerating final report...")
    
    report = f"""# Final Report: Paper Analysis

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
    
    # Add methodology
    report += generate_methodology_section()
    report += "\n---\n\n"
    
    # Add paper summary
    report += generate_paper_summary(paper_metadata)
    report += "\n---\n\n"
    
    # Add evaluation answers
    report += "## Evaluation Answers\n\n"
    if evaluation:
        # Remove the header from evaluation if it exists
        eval_content = evaluation.replace("# Evaluation Draft", "").replace("## Paper Analysis - Initial Answers", "").strip()
        report += eval_content
    else:
        report += "*Evaluation answers not yet generated*\n"
    
    report += "\n---\n\n"
    
    # Add appendix
    report += """## Appendix

### Repository Links

All scripts and data files are available in the GitHub repository:
- [Main Repository](https://github.com/[user-repo]/202511-AMMMA/)
- [Scripts](https://github.com/[user-repo]/202511-AMMMA/Docs/)

### Generated Files

- `llm_config.json` - LLM configuration
- `scopus_results.json` - Search results
- `graded_papers.json` - Scored papers
- `top_20_papers.md` - Top 20 ranked papers
- `selected_paper/` - Selected paper files
  - `paper.pdf` - Full text PDF
  - `paper_text.txt` - Extracted text
  - `paper_metadata.json` - Paper metadata
- `evaluation_draft.md` - Initial evaluation
- `evaluation_draft_v2.md` - First revision
- `evaluation_final.md` - Final evaluation
- `adversarial_critique_round1.md` - First critique
- `adversarial_critique_round2.md` - Second critique
- `shortcomings_assessment.md` - Final assessment

### Contact

For questions about this analysis, please contact [your email].
"""
    
    # Save report
    output_path = config.OUTPUT_FILES['final_report']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ Final report generated: {output_path}")
    
    print("\n" + "="*60)
    print("✓ PHASE 5 COMPLETE")
    print("="*60)
    print(f"\nFinal report saved to: {output_path.name}")
    print("\nYou can now proceed to Phase 6 (Presentation Creation)")
    
    return True

if __name__ == "__main__":
    main()
