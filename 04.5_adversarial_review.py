"""
Phase 4.5: Adversarial Review & Refinement
Two iterations of Devil's Advocate critique and Development LLM refinement.
"""

import json
from pathlib import Path
from typing import Dict, List
import config
import utils

def load_llm_config() -> Dict:
    """Load LLM configuration from Phase 0."""
    try:
        return utils.load_json(config.OUTPUT_FILES['llm_config'])
    except FileNotFoundError:
        print("❌ ERROR: llm_config.json not found!")
        return None

def load_evaluation_draft() -> str:
    """Load evaluation draft from Phase 4."""
    draft_path = config.OUTPUT_FILES['evaluation_draft']
    try:
        with open(draft_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ ERROR: evaluation_draft.md not found!")
        print("Please run Phase 4 (04_answer_evaluation.py) first.")
        return ""

def call_devils_advocate_llm(prompt: str, llm_config: Dict) -> str:
    """
    Call the Devil's Advocate LLM for critical review.
    Placeholder for actual API integration.
    """
    provider = llm_config['devils_advocate']['provider']
    model = llm_config['devils_advocate']['model_id']
    
    # Placeholder response
    return f"[PLACEHOLDER: Critical review from {provider} {model}]"

def call_development_llm(prompt: str, llm_config: Dict) -> str:
    """
    Call the Development LLM for refinement.
    Placeholder for actual API integration.
    """
    provider = llm_config['development']['provider']
    model = llm_config['development']['model_id']
    
    # Placeholder response
    return f"[PLACEHOLDER: Refined response from {provider} {model}]"

def devils_advocate_critique(draft: str, llm_config: Dict, round_num: int) -> str:
    """
    Devil's Advocate LLM critically reviews the evaluation draft.
    
    Args:
        draft: Current evaluation draft
        llm_config: LLM configuration
        round_num: Review round number (1 or 2)
        
    Returns:
        Critical review text
    """
    print(f"\n[Round {round_num}] Devil's Advocate reviewing...")
    
    prompt = f"""You are a critical reviewer for an academic paper analysis. Your role is to challenge the answers and identify weaknesses.

Review the following evaluation draft and provide critical feedback:

{draft}

For each answer, identify:
1. Logical gaps or unsupported claims
2. Missing evidence or citations from the paper
3. Overgeneralizations or assumptions
4. Areas where the answer could be more specific
5. Questions that are not adequately addressed

Be constructive but thorough in your critique. Focus on improving the quality and accuracy of the analysis.
"""
    
    critique = call_devils_advocate_llm(prompt, llm_config)
    return critique

def development_llm_refinement(draft: str, critique: str, llm_config: Dict, round_num: int) -> str:
    """
    Development LLM refines answers based on Devil's Advocate critique.
    
    Args:
        draft: Current evaluation draft
        critique: Devil's Advocate critique
        llm_config: LLM configuration
        round_num: Refinement round number (1 or 2)
        
    Returns:
        Refined evaluation text
    """
    print(f"\n[Round {round_num}] Development LLM refining...")
    
    prompt = f"""You are refining an academic paper analysis based on critical feedback.

Original draft:
{draft}

Critical feedback:
{critique}

Please revise the answers to address all points raised in the feedback. For each answer:
1. Address the specific critiques
2. Add missing evidence or citations
3. Clarify any ambiguous points
4. Strengthen weak arguments
5. Update confidence scores based on the quality of evidence

Maintain the same format as the original draft.
"""
    
    refined = call_development_llm(prompt, llm_config)
    return refined

def save_critique(critique: str, round_num: int):
    """Save Devil's Advocate critique to file."""
    filename = f"adversarial_critique_round{round_num}.md"
    output_path = config.DOCS_DIR / filename
    
    content = f"# Adversarial Critique - Round {round_num}\n\n"
    content += critique
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Critique saved to: {filename}")

def save_refined_draft(draft: str, round_num: int):
    """Save refined evaluation draft to file."""
    if round_num == 1:
        filename = "evaluation_draft_v2.md"
    else:
        filename = "evaluation_final.md"
    
    output_path = config.DOCS_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(draft)
    
    print(f"✓ Refined draft saved to: {filename}")
    return output_path

def identify_shortcomings(final_draft: str, llm_config: Dict) -> Dict:
    """
    Identify remaining shortcomings and suggest alternatives if needed.
    
    Returns:
        Dictionary with shortcomings and alternative suggestions
    """
    print("\nIdentifying remaining shortcomings...")
    
    prompt = f"""Review this final evaluation and identify any remaining shortcomings or gaps:

{final_draft}

Provide:
1. List of remaining shortcomings (if any)
2. Overall assessment of how well the paper meets the class requirements
3. Recommendation: Is this paper suitable, or should we consider alternatives?
4. If alternatives needed, what specific criteria should we prioritize?
"""
    
    assessment = call_development_llm(prompt, llm_config)
    
    return {
        'shortcomings': assessment,
        'recommendation': '[PLACEHOLDER: Suitable/Consider alternatives]',
        'alternative_criteria': '[PLACEHOLDER: Criteria if alternatives needed]'
    }

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 4.5: ADVERSARIAL REVIEW & REFINEMENT")
    print("="*60)
    
    # Load LLM configuration
    llm_config = load_llm_config()
    if not llm_config:
        return False
    
    print(f"\nDevelopment LLM: {llm_config['development']['provider']} - {llm_config['development']['model_key']}")
    print(f"Devil's Advocate LLM: {llm_config['devils_advocate']['provider']} - {llm_config['devils_advocate']['model_key']}")
    
    # Load initial draft
    current_draft = load_evaluation_draft()
    if not current_draft:
        return False
    
    print("✓ Loaded evaluation draft")
    
    # ITERATION 1
    print("\n" + "="*60)
    print("ITERATION 1")
    print("="*60)
    
    # Devil's Advocate critique round 1
    critique_1 = devils_advocate_critique(current_draft, llm_config, 1)
    save_critique(critique_1, 1)
    
    # Development LLM refinement round 1
    refined_draft_1 = development_llm_refinement(current_draft, critique_1, llm_config, 1)
    save_refined_draft(refined_draft_1, 1)
    
    # ITERATION 2
    print("\n" + "="*60)
    print("ITERATION 2")
    print("="*60)
    
    # Devil's Advocate critique round 2
    critique_2 = devils_advocate_critique(refined_draft_1, llm_config, 2)
    save_critique(critique_2, 2)
    
    # Development LLM final refinement
    final_draft = development_llm_refinement(refined_draft_1, critique_2, llm_config, 2)
    final_path = save_refined_draft(final_draft, 2)
    
    # Identify remaining shortcomings
    assessment = identify_shortcomings(final_draft, llm_config)
    
    # Save assessment
    assessment_path = config.DOCS_DIR / "shortcomings_assessment.md"
    with open(assessment_path, 'w', encoding='utf-8') as f:
        f.write("# Shortcomings Assessment\n\n")
        f.write(assessment['shortcomings'])
    
    print(f"\n✓ Assessment saved to: shortcomings_assessment.md")
    
    print("\n" + "="*60)
    print("✓ PHASE 4.5 COMPLETE")
    print("="*60)
    print("\nCompleted 2 iterations of adversarial review")
    print(f"Final evaluation: {final_path.name}")
    print(f"Recommendation: {assessment['recommendation']}")
    print("\nYou can now proceed to Phase 5 (Final Report)")
    
    return True

if __name__ == "__main__":
    main()
