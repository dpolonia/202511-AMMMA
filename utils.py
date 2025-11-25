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
import os
import time

def get_user_input(prompt_text: str, default: str = None) -> str:
    """
    Get input from user or from environment variable if in demo mode.
    
    Args:
        prompt_text: Text to display to user
        default: Default value if user just presses Enter (or for demo fallback)
        
    Returns:
        Input string
    """
    demo_inputs_env = os.getenv("AMMMA_DEMO_INPUTS")
    
    if demo_inputs_env:
        try:
            # Parse JSON list of inputs
            inputs = json.loads(demo_inputs_env)
            
            # Get the next input
            if inputs:
                next_input = inputs.pop(0)
                
                # Update the environment variable for the next call
                os.environ["AMMMA_DEMO_INPUTS"] = json.dumps(inputs)
                
                print(f"{prompt_text} {next_input} (AUTO-DEMO)")
                time.sleep(0.5) # Small delay for readability
                return next_input
        except Exception as e:
            print(f"Error parsing demo inputs: {e}")
            
    # Standard input
    return input(prompt_text)

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
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠️ pdftotext failed or not found ({e}). Trying pypdf fallback...")
        try:
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Save to output path if requested
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
            
            return text
        except ImportError:
            print("✗ pypdf not installed. Please install it: pip install pypdf")
            return ""
        except Exception as e2:
            print(f"✗ pypdf extraction failed: {e2}")
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

class TokenTracker:
    """
    Tracks token usage and calculates costs for LLM calls.
    Singleton instance used across the application.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenTracker, cls).__new__(cls)
            cls._instance.usage = {}  # {model_name: {'input': 0, 'output': 0, 'calls': 0}}
            cls._instance.alerts = {} # {model_name: last_alert_threshold}
        return cls._instance
    
    def track(self, model: str, input_tokens: int, output_tokens: int):
        """Record token usage for a model."""
        if model not in self.usage:
            self.usage[model] = {'input': 0, 'output': 0, 'calls': 0}
            self.alerts[model] = 0
            
        self.usage[model]['input'] += input_tokens
        self.usage[model]['output'] += output_tokens
        self.usage[model]['calls'] += 1
        
        # Check for alerts (every 100k total tokens)
        total_tokens = self.usage[model]['input'] + self.usage[model]['output']
        threshold = total_tokens // 100000
        
        if threshold > self.alerts[model]:
            self.alerts[model] = threshold
            print(f"\n[COST ALERT] Usage for {model} exceeded {threshold * 100000} tokens.")
            cost = self.calculate_cost(model)
            print(f"Estimated cost so far: ${cost:.2f}")
    
    def calculate_cost(self, model: str) -> float:
        """Calculate estimated cost for a specific model."""
        if model not in self.usage:
            return 0.0
            
        pricing = config.LLM_PRICING.get(model, {"input": 0, "output": 0})
        
        input_cost = (self.usage[model]['input'] / 1_000_000) * pricing['input']
        output_cost = (self.usage[model]['output'] / 1_000_000) * pricing['output']
        
        return input_cost + output_cost
    
    def get_total_cost(self) -> float:
        """Calculate total cost across all models."""
        return sum(self.calculate_cost(model) for model in self.usage)
        
    def get_summary(self) -> Dict:
        """Get summary of usage and costs."""
        summary = {}
        for model, stats in self.usage.items():
            cost = self.calculate_cost(model)
            summary[model] = {
                'calls': stats['calls'],
                'input_tokens': stats['input_tokens'], # Fix: key is 'input' in usage dict
                'output_tokens': stats['output_tokens'], # Fix: key is 'output' in usage dict
                'total_tokens': stats['input'] + stats['output'],
                'estimated_cost': cost
            }
        return summary
    
    def save_report(self, filepath: Path):
        """Save usage report to JSON."""
        report = {
            'usage': self.usage,
            'costs': {model: self.calculate_cost(model) for model in self.usage},
            'total_cost': self.get_total_cost()
        }
        save_json(report, filepath)

# Global tracker instance
tracker = TokenTracker()

def estimate_tokens(text: str) -> int:
    """
    Estimate token count (approx 4 chars per token).
    In production, use tiktoken or provider-specific tokenizers.
    """
    if not text:
        return 0
    return len(text) // 4

def call_llm(prompt: str, provider: str, model: str) -> str:
    """
    Centralized function to call LLMs with token tracking.
    
    Args:
        prompt: The prompt to send
        provider: LLM provider (anthropic, openai, google, xai)
        model: Model identifier
        
    Returns:
        LLM response text
    """
    # Estimate input tokens
    input_tokens = estimate_tokens(prompt)
    
    # Placeholder for actual API call
    # In production, this would call the specific provider API
    response = f"[PLACEHOLDER: Response from {provider} {model}]\n\nThis is a simulated response to demonstrate the workflow."
    
    # Estimate output tokens
    output_tokens = estimate_tokens(response)
    
    # Track usage
    tracker.track(model, input_tokens, output_tokens)
    
    return response
