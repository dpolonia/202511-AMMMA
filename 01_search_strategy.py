"""
Phase 1: Search Strategy & Data Retrieval
Define and execute Scopus search query.
"""

import json
from typing import List, Dict
import config
import utils

def build_search_query(strict: bool = True) -> str:
    """
    Build Scopus search query.
    
    Args:
        strict: If True, include all criteria. If False, relax PhD scope requirements.
        
    Returns:
        Scopus query string
    """
    # Fundamental criteria (non-negotiable)
    multilevel_terms = " OR ".join([f'"{term}"' for term in config.SEARCH_KEYWORDS['fundamental']['multilevel']])
    mixed_methods_terms = " OR ".join([f'"{term}"' for term in config.SEARCH_KEYWORDS['fundamental']['mixed_methods']])
    
    fundamental_query = f"({multilevel_terms}) AND ({mixed_methods_terms})"
    
    if not strict:
        # Relaxed query: only fundamental criteria
        return fundamental_query
    
    # Nice-to-have criteria (PhD scope)
    vbhc_terms = " OR ".join([f'"{term}"' for term in config.SEARCH_KEYWORDS['nice_to_have']['vbhc']])
    context_terms = " OR ".join([f'"{term}"' for term in config.SEARCH_KEYWORDS['nice_to_have']['context']])
    
    phd_scope_query = f"({vbhc_terms}) AND ({context_terms})"
    
    # Combined query
    full_query = f"{fundamental_query} AND {phd_scope_query}"
    
    return full_query

def execute_scopus_search(max_results: int = 200) -> List[Dict]:
    """
    Execute Scopus search with fallback strategy.
    
    Args:
        max_results: Maximum number of results to retrieve
        
    Returns:
        List of paper dictionaries
    """
    print("\n" + "="*60)
    print("EXECUTING SCOPUS SEARCH")
    print("="*60)
    
    # Try strict query first
    print("\n[1/2] Attempting strict search (all criteria)...")
    strict_query = build_search_query(strict=True)
    print(f"Query: {strict_query[:100]}...")
    
    results = utils.scopus_search(strict_query, config.SCOPUS_API_KEY, max_results)
    
    if len(results) < 20:
        print(f"\n⚠ Only {len(results)} results found with strict criteria.")
        print("[2/2] Attempting relaxed search (fundamental criteria only)...")
        
        relaxed_query = build_search_query(strict=False)
        print(f"Query: {relaxed_query[:100]}...")
        
        results = utils.scopus_search(relaxed_query, config.SCOPUS_API_KEY, max_results)
    
    print(f"\n✓ Retrieved {len(results)} papers from Scopus")
    return results

def parse_scopus_results(results: List[Dict]) -> List[Dict]:
    """
    Parse and structure Scopus results.
    
    Args:
        results: Raw Scopus API results
        
    Returns:
        List of structured paper dictionaries
    """
    papers = []
    
    for entry in results:
        paper = {
            'scopus_id': entry.get('dc:identifier', '').replace('SCOPUS_ID:', ''),
            'title': entry.get('dc:title', 'N/A'),
            'authors': entry.get('dc:creator', 'N/A'),
            'publication_name': entry.get('prism:publicationName', 'N/A'),
            'cover_date': entry.get('prism:coverDate', 'N/A'),
            'doi': entry.get('prism:doi', 'N/A'),
            'issn': entry.get('prism:issn', 'N/A'),
            'eissn': entry.get('prism:eIssn', 'N/A'),
            'cited_by_count': int(entry.get('citedby-count', 0)),
            'abstract': entry.get('dc:description', 'N/A'),
            'link': entry.get('link', [{}])[0].get('@href', 'N/A'),
            'affiliation': entry.get('affiliation', [{}])[0].get('affilname', 'N/A') if entry.get('affiliation') else 'N/A',
        }
        papers.append(paper)
    
    return papers

def save_results(papers: List[Dict]):
    """Save search results to JSON file."""
    output_path = config.OUTPUT_FILES['scopus_results']
    utils.save_json(papers, output_path)
    print(f"\n✓ Results saved to: {output_path}")

def display_summary(papers: List[Dict]):
    """Display search results summary."""
    print("\n" + "="*60)
    print("SEARCH RESULTS SUMMARY")
    print("="*60)
    
    print(f"\nTotal papers retrieved: {len(papers)}")
    
    if papers:
        print(f"\nSample papers:")
        for i, paper in enumerate(papers[:5], 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {paper['authors']}")
            print(f"   Journal: {paper['publication_name']}")
            print(f"   Year: {paper['cover_date'][:4] if paper['cover_date'] != 'N/A' else 'N/A'}")
            print(f"   Citations: {paper['cited_by_count']}")

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 1: SEARCH STRATEGY & DATA RETRIEVAL")
    print("="*60)
    
    # Check API key
    if not config.SCOPUS_API_KEY:
        print("\n❌ ERROR: SCOPUS_API_KEY not found in .env file!")
        return False
    
    # Execute search
    raw_results = execute_scopus_search(max_results=200)
    
    if not raw_results:
        print("\n❌ No results found. Please check your search criteria or API key.")
        return False
    
    # Parse results
    print("\nParsing results...")
    papers = parse_scopus_results(raw_results)
    
    # Save results
    save_results(papers)
    
    # Display summary
    display_summary(papers)
    
    print("\n" + "="*60)
    print("✓ PHASE 1 COMPLETE")
    print("="*60)
    print(f"\nRetrieved and saved {len(papers)} papers")
    print("You can now proceed to Phase 2 (Grading Algorithm)")
    
    return True

if __name__ == "__main__":
    main()
