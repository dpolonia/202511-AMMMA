import re

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
            elif line.startswith('N1  - '):
                match = re.search(r'Cited By: (\d+)', line)
                current_article['citations'] = int(match.group(1)) if match else 0

    if current_article: articles.append(current_article)
    
    # Score with breakdown
    for art in articles:
        breakdown = {}
        text = (art.get('title', '') + ' ' + art.get('abstract', '')).lower()
        
        # Multilevel
        if any(x in text for x in ['multilevel', 'multi-level', 'hierarchical linear', 'nested model']):
            breakdown['Multilevel'] = 10
        elif 'hierarchical' in text:
            breakdown['Hierarchical (fallback)'] = 5
        else:
            breakdown['Multilevel'] = 0
            
        # Mixed Methods
        if 'mixed method' in text:
            breakdown['Mixed Methods'] = 10
        elif 'qualitative' in text and 'quantitative' in text:
            breakdown['Qual + Quant'] = 5
        else:
            breakdown['Mixed Methods'] = 0
            
        # VBHC
        if any(x in text for x in ['vbhc', 'value-based']):
            breakdown['VBHC/Value-Based'] = 5
        else:
            breakdown['VBHC/Value-Based'] = 0
            
        # Context
        if any(x in text for x in ['portugal', 'portuguese']):
            breakdown['Portugal'] = 5
        elif 'nhs' in text or 'national health service' in text:
            breakdown['NHS'] = 3
        else:
            breakdown['Context'] = 0
            
        # Citations
        cit_score = min(art.get('citations', 0), 10) * 0.5
        breakdown['Citations'] = cit_score
        
        art['breakdown'] = breakdown
        art['score'] = sum(breakdown.values())
        
    return sorted(articles, key=lambda x: x['score'], reverse=True)[:10]

def main():
    ris_path = r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\scopus.ris'
    top_articles = parse_ris_top_10(ris_path)
    
    with open(r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\05_score_breakdown.md', 'w', encoding='utf-8') as f:
        f.write("# Top 10 Articles - Score Breakdown\n\n")
        
        for i, art in enumerate(top_articles, 1):
            f.write(f"## {i}. {art.get('title', 'No Title')}\n\n")
            f.write(f"**Total Relevance Score:** {art['score']}\n\n")
            
            f.write("### Score Breakdown\n\n")
            f.write("| Factor | Points |\n")
            f.write("|--------|--------|\n")
            
            for factor, points in art['breakdown'].items():
                f.write(f"| {factor} | {points} |\n")
            
            f.write(f"| **TOTAL** | **{art['score']}** |\n\n")
            
            f.write(f"**Journal:** {art.get('journal', 'N/A')} | **Year:** {art.get('year', 'N/A')}\n")
            f.write(f"**Citations:** {art.get('citations', 0)}\n\n")
            f.write("---\n\n")

if __name__ == "__main__":
    main()
