"""
Phase 2: Grading Algorithm
Score and rank papers based on multiple criteria.
"""

import json
from typing import List, Dict
import config
import utils

def customize_weights() -> Dict:
    """
    Allow user to customize grading weights interactively.
    
    Returns:
        Dictionary of customized weights
    """
    print("\n" + "="*60)
    print("CUSTOMIZE GRADING WEIGHTS")
    print("="*60)
    print("\nCurrent weights (Total: 100 points):")
    print("\nClass Relevance (50 points):")
    print(f"  - Multilevel (strong): {config.GRADING_WEIGHTS['class_relevance']['multilevel_strong']}")
    print(f"  - Multilevel (weak): {config.GRADING_WEIGHTS['class_relevance']['multilevel_weak']}")
    print(f"  - Mixed Methods (explicit): {config.GRADING_WEIGHTS['class_relevance']['mixed_methods_explicit']}")
    print(f"  - Mixed Methods (implicit): {config.GRADING_WEIGHTS['class_relevance']['mixed_methods_implicit']}")
    print("\nPhD Relevance (25 points):")
    print(f"  - VBHC: {config.GRADING_WEIGHTS['phd_relevance']['vbhc']}")
    print(f"  - NHS Context: {config.GRADING_WEIGHTS['phd_relevance']['nhs_context']}")
    print(f"  - Portugal: {config.GRADING_WEIGHTS['phd_relevance']['portugal']}")
    print("\nJournal Quality (20 points):")
    print(f"  - CiteScore: {config.GRADING_WEIGHTS['journal_quality']['citescore_max']}")
    print(f"  - SJR: {config.GRADING_WEIGHTS['journal_quality']['sjr_max']}")
    print("\nImpact (5 points):")
    print(f"  - Citations: {config.GRADING_WEIGHTS['impact']['citations_max']}")
    
    print("\n" + "-"*60)
    customize = utils.get_user_input("\nWould you like to customize these weights? (y/n): ").lower().strip()
    
    if customize != 'y':
        print("Using default weights.")
        return config.GRADING_WEIGHTS
    
    # Create a copy of default weights
    custom_weights = {
        "class_relevance": {},
        "phd_relevance": {},
        "journal_quality": {},
        "impact": {}
    }
    
    print("\n" + "="*60)
    print("ENTER CUSTOM WEIGHTS")
    print("="*60)
    print("(Press Enter to keep default value)")
    
    # Class Relevance
    print("\n--- Class Relevance ---")
    custom_weights['class_relevance']['multilevel_strong'] = get_weight_input(
        "Multilevel (strong)", config.GRADING_WEIGHTS['class_relevance']['multilevel_strong'])
    custom_weights['class_relevance']['multilevel_weak'] = get_weight_input(
        "Multilevel (weak)", config.GRADING_WEIGHTS['class_relevance']['multilevel_weak'])
    custom_weights['class_relevance']['mixed_methods_explicit'] = get_weight_input(
        "Mixed Methods (explicit)", config.GRADING_WEIGHTS['class_relevance']['mixed_methods_explicit'])
    custom_weights['class_relevance']['mixed_methods_implicit'] = get_weight_input(
        "Mixed Methods (implicit)", config.GRADING_WEIGHTS['class_relevance']['mixed_methods_implicit'])
    
    # PhD Relevance
    print("\n--- PhD Relevance ---")
    custom_weights['phd_relevance']['vbhc'] = get_weight_input(
        "VBHC", config.GRADING_WEIGHTS['phd_relevance']['vbhc'])
    custom_weights['phd_relevance']['nhs_context'] = get_weight_input(
        "NHS Context", config.GRADING_WEIGHTS['phd_relevance']['nhs_context'])
    custom_weights['phd_relevance']['portugal'] = get_weight_input(
        "Portugal", config.GRADING_WEIGHTS['phd_relevance']['portugal'])
    
    # Journal Quality
    print("\n--- Journal Quality ---")
    custom_weights['journal_quality']['citescore_max'] = get_weight_input(
        "CiteScore", config.GRADING_WEIGHTS['journal_quality']['citescore_max'])
    custom_weights['journal_quality']['sjr_max'] = get_weight_input(
        "SJR", config.GRADING_WEIGHTS['journal_quality']['sjr_max'])
    
    # Impact
    print("\n--- Impact ---")
    custom_weights['impact']['citations_max'] = get_weight_input(
        "Citations", config.GRADING_WEIGHTS['impact']['citations_max'])
    
    # Calculate and display total
    total = sum([
        sum(custom_weights['class_relevance'].values()),
        sum(custom_weights['phd_relevance'].values()),
        sum(custom_weights['journal_quality'].values()),
        sum(custom_weights['impact'].values())
    ])
    
    print(f"\n{'='*60}")
    print(f"Total weight: {total} points")
    
    if total != 100:
        print(f"⚠ WARNING: Total is {total}, not 100. Weights will be normalized.")
        # Normalize weights to sum to 100
        scale_factor = 100 / total
        for category in custom_weights:
            for key in custom_weights[category]:
                custom_weights[category][key] = round(custom_weights[category][key] * scale_factor, 2)
        print("✓ Weights normalized to 100 points")
    
    return custom_weights

def get_weight_input(name: str, default: float) -> float:
    """Get weight input from user with default fallback."""
    while True:
        user_input = utils.get_user_input(f"{name} [{default}]: ").strip()
        if not user_input:
            return default
        try:
            value = float(user_input)
            if value < 0:
                print("Please enter a non-negative number")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")

def score_multilevel_keywords(text: str, weights: Dict) -> Dict[str, int]:
    """
    Score paper based on multilevel analysis keywords.
    
    Args:
        text: Combined title + abstract text
        weights: Grading weights dictionary
        
    Returns:
        Dictionary with strong and weak scores
    """
    strong_keywords = ["hierarchical linear model", "HLM", "multilevel model", "nested data"]
    weak_keywords = ["multilevel", "multi-level", "hierarchical"]
    
    strong_count = utils.count_keyword_matches(text, strong_keywords)
    weak_count = utils.count_keyword_matches(text, weak_keywords)
    
    # Strong keywords get full points, weak get partial
    strong_score = min(strong_count * 10, weights['class_relevance']['multilevel_strong'])
    weak_score = min(weak_count * 5, weights['class_relevance']['multilevel_weak'])
    
    return {
        'strong': strong_score,
        'weak': weak_score if strong_score == 0 else 0  # Don't double-count
    }

def score_mixed_methods(text: str, weights: Dict) -> Dict[str, int]:
    """
    Score paper based on mixed methods keywords.
    
    Args:
        text: Combined title + abstract text
        weights: Grading weights dictionary
        
    Returns:
        Dictionary with explicit and implicit scores
    """
    explicit_keywords = ["mixed method", "mixed-method", "qualitative and quantitative"]
    implicit_keywords = ["multi-method", "triangulation", "convergent design"]
    
    explicit_count = utils.count_keyword_matches(text, explicit_keywords)
    implicit_count = utils.count_keyword_matches(text, implicit_keywords)
    
    explicit_score = min(explicit_count * 10, weights['class_relevance']['mixed_methods_explicit'])
    implicit_score = min(implicit_count * 5, weights['class_relevance']['mixed_methods_implicit'])
    
    return {
        'explicit': explicit_score,
        'implicit': implicit_score if explicit_score == 0 else 0
    }

def score_vbhc_relevance(text: str, weights: Dict) -> int:
    """Score paper based on VBHC keywords."""
    vbhc_keywords = config.SEARCH_KEYWORDS['nice_to_have']['vbhc']
    count = utils.count_keyword_matches(text, vbhc_keywords)
    return min(count * 5, weights['phd_relevance']['vbhc'])

def score_nhs_context(text: str, weights: Dict) -> int:
    """Score paper based on NHS/Beveridgean context keywords."""
    context_keywords = config.SEARCH_KEYWORDS['nice_to_have']['context']
    count = utils.count_keyword_matches(text, context_keywords)
    return min(count * 5, weights['phd_relevance']['nhs_context'])

def score_portugal_specific(text: str, weights: Dict) -> int:
    """Score paper based on Portugal-specific keywords."""
    portugal_keywords = ["Portugal", "Portuguese"]
    count = utils.count_keyword_matches(text, portugal_keywords)
    return min(count * 5, weights['phd_relevance']['portugal'])

def score_journal_quality(issn: str, weights: Dict) -> Dict[str, float]:
    """
    Score journal based on CiteScore and SJR.
    
    Args:
        issn: Journal ISSN
        weights: Grading weights dictionary
        
    Returns:
        Dictionary with citescore and sjr scores
    """
    metrics = utils.get_journal_metrics(issn, config.SCOPUS_API_KEY)
    
    # Normalize CiteScore (assume max ~20 for top journals)
    citescore = metrics.get('citescore', 'N/A')
    if citescore != 'N/A':
        try:
            citescore_normalized = min(float(citescore) / 20 * weights['journal_quality']['citescore_max'], 
                                      weights['journal_quality']['citescore_max'])
        except:
            citescore_normalized = 0
    else:
        citescore_normalized = 0
    
    # Normalize SJR (assume max ~5 for top journals)
    sjr = metrics.get('sjr', 'N/A')
    if sjr != 'N/A':
        try:
            sjr_normalized = min(float(sjr) / 5 * weights['journal_quality']['sjr_max'],
                                weights['journal_quality']['sjr_max'])
        except:
            sjr_normalized = 0
    else:
        sjr_normalized = 0
    
    return {
        'citescore': round(citescore_normalized, 2),
        'sjr': round(sjr_normalized, 2),
        'raw_citescore': citescore,
        'raw_sjr': sjr
    }

def score_citations(cited_by_count: int, weights: Dict, max_citations: int = 500) -> float:
    """
    Score paper based on citation count (normalized).
    
    Args:
        cited_by_count: Number of citations
        weights: Grading weights dictionary
        max_citations: Maximum citations for normalization
        
    Returns:
        Normalized citation score
    """
    normalized = min(cited_by_count / max_citations * weights['impact']['citations_max'],
                    weights['impact']['citations_max'])
    return round(normalized, 2)

def grade_paper(paper: Dict, weights: Dict = None) -> Dict:
    """
    Grade a single paper based on all criteria.
    
    Args:
        paper: Paper dictionary from Scopus
        weights: Custom weights dictionary (uses config.GRADING_WEIGHTS if None)
        
    Returns:
        Paper dictionary with added grading information
    """
    if weights is None:
        weights = config.GRADING_WEIGHTS
    
    # Combine title and abstract for keyword matching
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
    
    # Score each category
    multilevel_scores = score_multilevel_keywords(text, weights)
    mixed_methods_scores = score_mixed_methods(text, weights)
    vbhc_score = score_vbhc_relevance(text, weights)
    nhs_score = score_nhs_context(text, weights)
    portugal_score = score_portugal_specific(text, weights)
    
    # Journal quality (use ISSN or eISSN)
    issn = paper.get('issn') or paper.get('eissn', 'N/A')
    journal_scores = score_journal_quality(issn, weights) if issn != 'N/A' else {'citescore': 0, 'sjr': 0, 'raw_citescore': 'N/A', 'raw_sjr': 'N/A'}
    
    # Citation score
    citation_score = score_citations(paper.get('cited_by_count', 0), weights)
    
    # Calculate class relevance subtotal
    class_relevance_subtotal = (
        multilevel_scores['strong'] +
        multilevel_scores['weak'] +
        mixed_methods_scores['explicit'] +
        mixed_methods_scores['implicit']
    )
    
    # Check minimum threshold: Class Relevance cannot be zero
    if class_relevance_subtotal == 0:
        total_score = 0
    else:
        # Calculate total score normally
        total_score = (
            class_relevance_subtotal +
            vbhc_score +
            nhs_score +
            portugal_score +
            journal_scores['citescore'] +
            journal_scores['sjr'] +
            citation_score
        )
    
    # Add grading information to paper
    paper['grading'] = {
        'total_score': round(total_score, 2),
        'breakdown': {
            'class_relevance': {
                'multilevel_strong': multilevel_scores['strong'],
                'multilevel_weak': multilevel_scores['weak'],
                'mixed_methods_explicit': mixed_methods_scores['explicit'],
                'mixed_methods_implicit': mixed_methods_scores['implicit'],
                'subtotal': multilevel_scores['strong'] + multilevel_scores['weak'] + 
                           mixed_methods_scores['explicit'] + mixed_methods_scores['implicit']
            },
            'phd_relevance': {
                'vbhc': vbhc_score,
                'nhs_context': nhs_score,
                'portugal': portugal_score,
                'subtotal': vbhc_score + nhs_score + portugal_score
            },
            'journal_quality': {
                'citescore': journal_scores['citescore'],
                'sjr': journal_scores['sjr'],
                'raw_citescore': journal_scores['raw_citescore'],
                'raw_sjr': journal_scores['raw_sjr'],
                'subtotal': journal_scores['citescore'] + journal_scores['sjr']
            },
            'impact': {
                'citations': citation_score,
                'raw_citations': paper.get('cited_by_count', 0),
                'subtotal': citation_score
            }
        }
    }
    
    return paper

def grade_all_papers(papers: List[Dict], weights: Dict = None) -> List[Dict]:
    """Grade all papers and sort by total score."""
    print("\n" + "="*60)
    print("GRADING PAPERS")
    print("="*60)
    
    graded_papers = []
    for i, paper in enumerate(papers, 1):
        if i % 10 == 0:
            print(f"Graded {i}/{len(papers)} papers...")
        graded_paper = grade_paper(paper, weights)
        graded_papers.append(graded_paper)
    
    # Sort by total score (descending)
    graded_papers.sort(key=lambda x: x['grading']['total_score'], reverse=True)
    
    print(f"\n✓ Graded {len(graded_papers)} papers")
    return graded_papers

def generate_top_20_report(graded_papers: List[Dict]):
    """Generate markdown report for top 20 papers."""
    top_20 = graded_papers[:20]
    
    report = "# Top 20 Papers - Grading Report\n\n"
    report += f"**Total papers graded**: {len(graded_papers)}\n\n"
    report += "---\n\n"
    
    for i, paper in enumerate(top_20, 1):
        grading = paper['grading']
        breakdown = grading['breakdown']
        
        report += f"## {i}. {paper['title']}\n\n"
        report += f"**Total Score**: {grading['total_score']}/100\n\n"
        report += f"**Authors**: {paper['authors']}\n\n"
        report += f"**Journal**: {paper['publication_name']}\n\n"
        report += f"**Year**: {paper['cover_date'][:4] if paper['cover_date'] != 'N/A' else 'N/A'}\n\n"
        report += f"**Citations**: {breakdown['impact']['raw_citations']}\n\n"
        report += f"**DOI**: {paper['doi']}\n\n"
        
        report += "### Score Breakdown\n\n"
        report += f"- **Class Relevance** ({breakdown['class_relevance']['subtotal']}/60):\n"
        report += f"  - Multilevel (strong): {breakdown['class_relevance']['multilevel_strong']}/20\n"
        report += f"  - Multilevel (weak): {breakdown['class_relevance']['multilevel_weak']}/10\n"
        report += f"  - Mixed Methods (explicit): {breakdown['class_relevance']['mixed_methods_explicit']}/20\n"
        report += f"  - Mixed Methods (implicit): {breakdown['class_relevance']['mixed_methods_implicit']}/10\n\n"
        
        report += f"- **PhD Relevance** ({breakdown['phd_relevance']['subtotal']}/25):\n"
        report += f"  - VBHC: {breakdown['phd_relevance']['vbhc']}/10\n"
        report += f"  - NHS Context: {breakdown['phd_relevance']['nhs_context']}/10\n"
        report += f"  - Portugal: {breakdown['phd_relevance']['portugal']}/5\n\n"
        
        report += f"- **Journal Quality** ({breakdown['journal_quality']['subtotal']}/25):\n"
        report += f"  - CiteScore: {breakdown['journal_quality']['citescore']}/15 (raw: {breakdown['journal_quality']['raw_citescore']})\n"
        report += f"  - SJR: {breakdown['journal_quality']['sjr']}/10 (raw: {breakdown['journal_quality']['raw_sjr']})\n\n"
        
        report += f"- **Impact** ({breakdown['impact']['subtotal']}/10):\n"
        report += f"  - Citations: {breakdown['impact']['citations']}/10 (raw: {breakdown['impact']['raw_citations']})\n\n"
        
        if paper.get('abstract') != 'N/A':
            abstract_preview = paper['abstract'][:300] + "..." if len(paper['abstract']) > 300 else paper['abstract']
            report += f"**Abstract**: {abstract_preview}\n\n"
        
        report += "---\n\n"
    
    # Save report
    output_path = config.OUTPUT_FILES['top_20_papers']
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ Top 20 report saved to: {output_path}")

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 2: GRADING ALGORITHM")
    print("="*60)
    
    # Load papers from Phase 1
    try:
        papers = utils.load_json(config.OUTPUT_FILES['scopus_results'])
    except FileNotFoundError:
        print("\n❌ ERROR: scopus_results.json not found!")
        print("Please run Phase 1 (01_search_strategy.py) first.")
        return False
    
    # Customize weights
    custom_weights = customize_weights()
    
    # Grade all papers
    graded_papers = grade_all_papers(papers, custom_weights)
    
    # Save graded papers
    utils.save_json(graded_papers, config.OUTPUT_FILES['graded_papers'])
    print(f"✓ Graded papers saved to: {config.OUTPUT_FILES['graded_papers']}")
    
    # Generate top 20 report
    generate_top_20_report(graded_papers)
    
    # Display summary
    print("\n" + "="*60)
    print("TOP 5 PAPERS")
    print("="*60)
    for i, paper in enumerate(graded_papers[:5], 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Score: {paper['grading']['total_score']}/100")
        print(f"   Journal: {paper['publication_name']}")
        print(f"   Citations: {paper['cited_by_count']}")
    
    print("\n" + "="*60)
    print("✓ PHASE 2 COMPLETE")
    print("="*60)
    print(f"\nGraded {len(graded_papers)} papers")
    print(f"Top 20 report generated: {config.OUTPUT_FILES['top_20_papers']}")
    print("\nYou can now proceed to Phase 3 (Paper Retrieval)")
    
    return True

if __name__ == "__main__":
    main()
