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

### Generated Files & Workflow Chronology

The following files were generated during the analysis workflow, listed in chronological order of creation:

1. **`00_llm_config.json`** (Phase 0)
   - *Why*: Defines the selected LLM providers and models for Development and Devil's Advocate roles.
   - *When*: Created at the start of the workflow during configuration.

2. **`01_scopus_results.json`** (Phase 1)
   - *Why*: Contains raw metadata for all papers retrieved from Scopus based on search criteria.
   - *When*: Generated after executing the search strategy.

3. **`02_graded_papers.json`** (Phase 2)
   - *Why*: Stores grading scores and detailed breakdowns for all retrieved papers.
   - *When*: Created after applying the grading algorithm to the search results.

4. **`02_top_20_papers.md`** (Phase 2)
   - *Why*: Provides a human-readable ranking of the highest-scoring papers for user review.
   - *When*: Generated immediately after grading to assist in paper selection.

5. **`03_selected_paper/`** (Phase 3)
   - *Why*: Directory containing the chosen paper's full text (PDF & txt) and metadata.
   - *When*: Created after the user selects a paper for deep analysis.
     - `paper.pdf`: Original PDF file.
     - `paper_text.txt`: Extracted text for LLM processing.
     - `paper_metadata.json`: Specific metadata for the selected paper.

6. **`04_evaluation_draft.md`** (Phase 4)
   - *Why*: The initial set of answers to the evaluation checklist generated by the Development LLM.
   - *When*: Created after the first pass of analysis on the extracted text.

7. **`04.5_adversarial_reviews/`** (Phase 4.5)
   - *Why*: Contains the iterative dialogue between Devil's Advocate and Development LLMs.
   - *When*: Generated during the interactive review process.
     - `iteration_HHMMSS/`: Timestamped folder for each review session.
     - `adversarial_critique_roundX.md`: Critical feedback from Devil's Advocate.
     - `evaluation_draft_vX.md`: Refined answers after addressing critiques.

8. **`05_evaluation_final.md`** (Phase 4.5)
   - *Why*: The polished, final version of the evaluation after all refinement rounds.
   - *When*: Saved upon completion of the adversarial review phase.

9. **`05_shortcomings_assessment.md`** (Phase 4.5)
   - *Why*: A final honest assessment of any remaining gaps or limitations in the paper.
   - *When*: Generated as the last step of the review phase.

10. **`05_final_report.md`** (Phase 5)
    - *Why*: This document; the comprehensive deliverable summarizing the entire analysis.
    - *When*: Generated after all analysis and evaluation is complete.

11. **`05_llm_usage.json`** (Phase 5)
    - *Why*: Detailed log of token usage and estimated costs for the run.
    - *When*: Saved alongside the final report for auditing.

12. **`06_presentation.md`** (Phase 6)
    - *Why*: An 8-slide presentation summary ready for class delivery.
    - *When*: Generated as the final output of the workflow.

### Contact

For questions about this analysis, please contact [your email].
"""

    # Add Token Usage Appendix
    report += "\n\n# Appendix: Token Usage & Cost Analysis\n\n"
    report += "## Estimated Usage Breakdown\n\n"
    report += "| Model | Calls | Input Tokens | Output Tokens | Total Tokens | Est. Cost |\n"
    report += "|-------|-------|--------------|---------------|--------------|-----------|\n"
    
    total_cost = 0.0
    
    for model, stats in utils.tracker.usage.items():
        cost = utils.tracker.calculate_cost(model)
        total_cost += cost
        report += f"| {model} | {stats['calls']} | {stats['input']:,} | {stats['output']:,} | {stats['input'] + stats['output']:,} | ${cost:.4f} |\n"
    
    report += f"| **TOTAL** | | | | | **${total_cost:.4f}** |\n"
    
    report += "\n*Note: Token counts are estimated (approx. 4 chars/token). Costs are based on standard pricing.*"
    
    # Save report
    output_path = config.OUTPUT_FILES['final_report']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ Final report generated: {output_path}")
    
    # Save usage data separately
    usage_path = config.OUTPUT_DIR / "05_llm_usage.json"
    utils.tracker.save_report(usage_path)
    print(f"✓ Token usage data saved to: {usage_path}")
    
    print("\n" + "="*60)
    print("✓ PHASE 5 COMPLETE")
    print("="*60)
    print(f"\nFinal report saved to: {output_path.name}")
    print("\nYou can now proceed to Phase 6 (Presentation Creation)")
    
    return True

if __name__ == "__main__":
    main()
