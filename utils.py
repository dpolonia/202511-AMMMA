"""
Utility functions for the paper analysis workflow.
"""

import subprocess
import requests
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
import config

def extract_pdf_text(pdf_path: Path, output_path: Optional[Path] = None) -> str:
    """
    Extract text from PDF using pdftotext.
    
    Args:
        pdf_path: Path to PDF file
        output_path: Optional path to save extracted text
        
    Returns:
        Extracted text as string
    """
    if output_path is None:
        output_path = pdf_path.with_suffix('.txt')
    
    try:
        subprocess.run(
            ['pdftotext', str(pdf_path), str(output_path)],
            check=True,
            capture_output=True
        )
        
        with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        return text
    except subprocess.CalledProcessError as e:
        print(f"Error extracting PDF: {e}")
        return ""

def scopus_search(query: str, api_key: str, max_results: int = 200) -> List[Dict]:
    """
    Search Scopus API for papers.
    
    Args:
        query: Search query string
        api_key: Scopus API key
        max_results: Maximum number of results to retrieve
        
    Returns:
        List of paper dictionaries
    """
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }
    
    params = {
        'query': query,
        'count': min(max_results, 25),  # API limit per request
        'start': 0
    }
    
    all_results = []
    
    while len(all_results) < max_results:
        try:
            response = requests.get(
                config.SCOPUS_SEARCH_URL,
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Scopus API error: {response.status_code}")
                print(f"Response: {response.text}")
                break
            
            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])
            
            if not entries:
                break
            
            all_results.extend(entries)
            
            # Check if there are more results
            total_results = int(data.get('search-results', {}).get('opensearch:totalResults', 0))
            if len(all_results) >= total_results:
                break
            
            # Update start parameter for next page
            params['start'] += params['count']
            
        except Exception as e:
            print(f"Error during Scopus search: {e}")
            break
    
    return all_results[:max_results]

def get_journal_metrics(issn: str, api_key: str) -> Dict:
    """
    Get journal metrics from Scopus Serial Title API.
    
    Args:
        issn: Journal ISSN
        api_key: Scopus API key
        
    Returns:
        Dictionary with CiteScore, SJR, SNIP
    """
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(
            f"{config.SCOPUS_SERIAL_URL}/issn/{issn}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            entry = data.get('serial-metadata-response', {}).get('entry', [{}])[0]
            
            citescore = entry.get('citeScoreYearInfoList', {}).get('citeScoreCurrentMetric', 'N/A')
            sjr = entry.get('SJRList', {}).get('SJR', [{}])[0].get('$', 'N/A')
            snip = entry.get('SNIPList', {}).get('SNIP', [{}])[0].get('$', 'N/A')
            
            return {
                'citescore': citescore,
                'sjr': sjr,
                'snip': snip
            }
    except Exception as e:
        print(f"Error fetching journal metrics for ISSN {issn}: {e}")
    
    return {'citescore': 'N/A', 'sjr': 'N/A', 'snip': 'N/A'}

def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
    return text.strip()

def save_json(data: Dict or List, filepath: Path):
    """Save data to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: Path) -> Dict or List:
    """Load data from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_keyword_matches(text: str, keywords: List[str]) -> int:
    """
    Count how many keywords appear in text (case-insensitive).
    
    Args:
        text: Text to search
        keywords: List of keywords
        
    Returns:
        Number of keyword matches
    """
    text_lower = text.lower()
    return sum(1 for keyword in keywords if keyword.lower() in text_lower)
