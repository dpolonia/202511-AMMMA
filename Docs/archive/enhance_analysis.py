import requests
import os
import time
import re

# Load API Key
def load_api_key():
    with open(r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\.env', 'r') as f:
        for line in f:
            if line.startswith('SCOPUS_API_KEY='):
                return line.strip().split('=')[1]
    return None

API_KEY = load_api_key()
HEADERS = {
    'X-ELS-APIKey': API_KEY,
    'Accept': 'application/json'
}

def clean_title(title):
    # Remove special characters that might break the API query
    return re.sub(r'[^\w\s-]', '', title)

def get_scopus_data(title, doi=None):
    """Search for the article to get Scopus ID and basic metrics"""
    base_url = "https://api.elsevier.com/content/search/scopus"
    
    # Try DOI first if available
    if doi:
        query = f"DOI({doi})"
    else:
        # Clean title and use strict search
        cleaned = clean_title(title)
        query = f"TITLE({cleaned})"
        
    params = {
        'query': query,
        'count': 1,
        'view': 'COMPLETE'
    }
    
    try:
        response = requests.get(base_url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'search-results' in data and data['search-results']['opensearch:totalResults'] != '0':
                return data['search-results']['entry'][0]
            else:
                print(f"No results for: {title[:30]}...")
        else:
            print(f"Search failed for {title[:30]}... Status: {response.status_code}")
    except Exception as e:
        print(f"Error searching for {title}: {e}")
    return None

def get_serial_metrics(issn):
    """Get Journal Metrics (CiteScore, SJR) using ISSN"""
    if not issn:
        return {}
        
    base_url = "https://api.elsevier.com/content/serial/title"
    params = {
        'issn': issn,
        'view': 'STANDARD'
    }
    
    try:
        response = requests.get(base_url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'serial-metadata-response' in data and 'entry' in data['serial-metadata-response']:
                entry = data['serial-metadata-response']['entry'][0]
                return {
                    'SJR': entry.get('SJRList', {}).get('SJR', [{}])[0].get('$', 'N/A'),
                    'CiteScore': entry.get('citeScoreYearInfoList', {}).get('citeScoreCurrentMetric', 'N/A'),
                    'SNIP': entry.get('SNIPList', {}).get('SNIP', [{}])[0].get('$', 'N/A')
                }
    except Exception as e:
        print(f"Error fetching serial metrics for {issn}: {e}")
    return {}

def parse_ris_top_10(file_path):
    articles = []
    current_article = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line.startswith('TY  - '):
                if current_article: articles.append(current_article)
                current_article = {'raw_text': ''}
            current_article['raw_text'] = current_article.get('raw_text', '') + line + '\n'
            if line.startswith('TI  - '): current_article['title'] = line[6:]
            elif line.startswith('AB  - '): current_article['abstract'] = line[6:]
            elif line.startswith('AU  - '): current_article.setdefault('authors', []).append(line[6:])
            elif line.startswith('PY  - '): current_article['year'] = line[6:]
            elif line.startswith('T2  - '): current_article['journal'] = line[6:]
            elif line.startswith('SN  - '): current_article['issn'] = line[6:].split(' ')[0] # Simple extract
            elif line.startswith('DO  - '): current_article['doi'] = line[6:]
            elif line.startswith('N1  - '):
                match = re.search(r'Cited By: (\d+)', line)
                current_article['citations'] = int(match.group(1)) if match else 0

    if current_article: articles.append(current_article)
    
    # Score
    for art in articles:
        score = 0
        text = (art.get('title', '') + ' ' + art.get('abstract', '')).lower()
        if any(x in text for x in ['multilevel', 'multi-level', 'hierarchical linear', 'nested model']): score += 10
        elif 'hierarchical' in text: score += 5
        if 'mixed method' in text: score += 10
        elif 'qualitative' in text and 'quantitative' in text: score += 5
        if any(x in text for x in ['vbhc', 'value-based']): score += 5
        if any(x in text for x in ['portugal', 'portuguese']): score += 5
        elif 'nhs' in text: score += 3
        score += min(art.get('citations', 0), 10) * 0.5
        art['score'] = score
        
    return sorted(articles, key=lambda x: x['score'], reverse=True)[:10]

def main():
    ris_path = r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\scopus.ris'
    top_articles = parse_ris_top_10(ris_path)
    
    with open(r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\04_enhanced_analysis.md', 'w', encoding='utf-8') as f:
        f.write("# Top 10 Articles - Enhanced Analysis\n\n")
        
        for i, art in enumerate(top_articles, 1):
            print(f"Processing {i}/10: {art.get('title')[:30]}...")
            
            # Fetch Scopus Data
            scopus_entry = get_scopus_data(art.get('title'), art.get('doi'))
            metrics = {}
            
            citations = art.get('citations', 0)
            ref_count = 'N/A'
            scopus_link = 'N/A'
            issn = art.get('issn') # Start with RIS ISSN
            
            if scopus_entry:
                citations = scopus_entry.get('citedby-count', citations)
                ref_count = scopus_entry.get('ref-count', 'N/A')
                scopus_link = next((l['@href'] for l in scopus_entry.get('link', []) if l['@ref'] == 'scopus'), 'N/A')
                
                # Update ISSN from API if available
                api_issn = scopus_entry.get('prism:issn') or scopus_entry.get('prism:eIssn')
                if api_issn:
                    issn = api_issn
            
            # Get Journal Metrics if we have an ISSN
            if issn:
                metrics = get_serial_metrics(issn)
            else:
                print(f"No ISSN found for article {i}")
            
            f.write(f"## {i}. {art.get('title', 'No Title')}\n")
            f.write(f"**Journal:** {art.get('journal', 'N/A')} | **Year:** {art.get('year', 'N/A')}\n")
            f.write(f"**Authors:** {', '.join(art.get('authors', [])[:3])} et al.\n")
            f.write(f"**Relevance Score:** {art['score']}\n\n")
            
            f.write("### Metrics\n")
            f.write(f"- **Citations:** {citations}\n")
            f.write(f"- **Cited References:** {ref_count}\n")
            f.write(f"- **CiteScore:** {metrics.get('CiteScore', 'N/A')}\n")
            f.write(f"- **SJR:** {metrics.get('SJR', 'N/A')}\n")
            f.write(f"- **SNIP:** {metrics.get('SNIP', 'N/A')}\n")
            if scopus_link != 'N/A':
                f.write(f"- [View in Scopus]({scopus_link})\n")
            
            f.write(f"\n**Abstract Snippet:** {art.get('abstract', '')[:300]}...\n\n")
            f.write("---\n\n")
            
            time.sleep(0.5) # Rate limit politeness

if __name__ == "__main__":
    main()
