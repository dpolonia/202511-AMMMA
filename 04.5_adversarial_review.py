"""
Phase 4.5: Adversarial Review & Refinement
Interactive dialogue between Devil's Advocate and Development LLM with user control.
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

def get_user_comments() -> str:
    """
    Get additional comments from user to add to Devil's Advocate critique.
    
    Returns:
        User comments or empty string if none
    """
    print("\n" + "="*60)
    print("USER COMMENTS")
    print("="*60)
    print("\nYou can add your own comments on top of the Devil's Advocate critique.")
    print("This allows you to provide additional guidance or specific concerns.")
    print("\nOptions:")
    print("  1. Enter comments (type your feedback, then press Enter twice)")
    print("  2. Skip (press Enter to continue without comments)")
    
    choice = input("\nAdd comments? (y/n): ").lower().strip()
    
    if choice != 'y':
        return ""
    
    print("\nEnter your comments (press Enter twice when done):")
    print("-" * 60)
    
    lines = []
    empty_count = 0
    
    while True:
        line = input()
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)
    
    comments = "\n".join(lines).strip()
    
    if comments:
        print(f"\n✓ Added {len(lines)} lines of comments")
    
    return comments

def devils_advocate_critique(draft: str, llm_config: Dict, round_num: int) -> str:
    """
    Devil's Advocate LLM critically reviews the evaluation draft.
    
    Args:
        draft: Current evaluation draft
        llm_config: LLM configuration
        round_num: Review round number
        
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

def combine_critique_with_user_comments(critique: str, user_comments: str) -> str:
    """
    Combine Devil's Advocate critique with user comments.
    
    Args:
        critique: Devil's Advocate critique
        user_comments: User's additional comments
        
    Returns:
        Combined critique
    """
    if not user_comments:
        return critique
    
    combined = f"""# Combined Critique

## User Comments

{user_comments}

---

## Devil's Advocate Review

{critique}
"""
    return combined

def development_llm_refinement(draft: str, critique: str, llm_config: Dict, round_num: int) -> str:
    """
    Development LLM refines answers based on critique.
    
    Args:
        draft: Current evaluation draft
        critique: Combined critique (Devil's Advocate + user comments)
        llm_config: LLM configuration
        round_num: Refinement round number
        
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
    """Save critique to file."""
    filename = f"adversarial_critique_round{round_num}.md"
    output_path = config.DOCS_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(critique)
    
    print(f"✓ Critique saved to: {filename}")

def save_refined_draft(draft: str, version: int) -> Path:
    """Save refined evaluation draft to file."""
    filename = f"evaluation_draft_v{version}.md"
    output_path = config.DOCS_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(draft)
    
    print(f"✓ Refined draft saved to: {filename}")
    return output_path

def user_wants_to_continue() -> bool:
    """
    Ask user if they want to continue with another iteration.
    
    Returns:
        True if user wants to continue, False otherwise
    """
    print("\n" + "="*60)
    print("CONTINUE DIALOGUE?")
    print("="*60)
    print("\nThe Development LLM has refined the evaluation based on the critique.")
    print("\nOptions:")
    print("  1. Continue - Start another round of critique and refinement")
    print("  2. Finalize - Accept current version as final")
    
    choice = input("\nContinue with another iteration? (y/n): ").lower().strip()
    
    return choice == 'y'

def finalize_evaluation(draft: str) -> Path:
    """
    Finalize the evaluation and save as final version.
    
    Args:
        draft: Final evaluation draft
        
    Returns:
        Path to final evaluation file
    """
    filename = "evaluation_final.md"
    output_path = config.DOCS_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(draft)
    
    print(f"\n✓ Final evaluation saved to: {filename}")
    return output_path

def identify_shortcomings(final_draft: str, llm_config: Dict) -> Dict:
    """
    Identify remaining shortcomings and suggest alternatives if needed.
    
    Returns:
        Dictionary with shortcomings and alternative suggestions
    """
    print("\n" + "="*60)
    print("FINAL ASSESSMENT")
    print("="*60)
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
    print("\nInteractive dialogue with user control")
    
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
    
    # Interactive dialogue loop
    round_num = 1
    version = 1
    
    while True:
        print("\n" + "="*60)
        print(f"ITERATION {round_num}")
        print("="*60)
        
        # Devil's Advocate critique
        critique = devils_advocate_critique(current_draft, llm_config, round_num)
        
        # Get user comments
        user_comments = get_user_comments()
        
        # Combine critique with user comments
        combined_critique = combine_critique_with_user_comments(critique, user_comments)
        
        # Save combined critique
        save_critique(combined_critique, round_num)
        
        # Development LLM refinement
        refined_draft = development_llm_refinement(current_draft, combined_critique, llm_config, round_num)
        
        # Increment version and save
        version += 1
        save_refined_draft(refined_draft, version)
        
        # Ask user if they want to continue
        if not user_wants_to_continue():
            print("\n✓ User chose to finalize evaluation")
            current_draft = refined_draft
            break
        
        # Continue with next iteration
        print("\n✓ Starting next iteration...")
        current_draft = refined_draft
        round_num += 1
    
    # Finalize evaluation
    final_path = finalize_evaluation(current_draft)
    
    # Identify remaining shortcomings
    assessment = identify_shortcomings(current_draft, llm_config)
    
    # Save assessment
    assessment_path = config.DOCS_DIR / "shortcomings_assessment.md"
    with open(assessment_path, 'w', encoding='utf-8') as f:
        f.write("# Shortcomings Assessment\n\n")
        f.write(assessment['shortcomings'])
    
    print(f"✓ Assessment saved to: shortcomings_assessment.md")
    
    print("\n" + "="*60)
    print("✓ PHASE 4.5 COMPLETE")
    print("="*60)
    print(f"\nCompleted {round_num} iteration(s) of adversarial review")
    print(f"Final evaluation: {final_path.name}")
    print(f"Recommendation: {assessment['recommendation']}")
    print("\nYou can now proceed to Phase 5 (Final Report)")
    
    return True

if __name__ == "__main__":
    main()
