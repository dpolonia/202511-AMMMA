import re

def parse_ris(file_path):
    articles = []
    current_article = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('TY  - '):
                if current_article:
                    articles.append(current_article)
                current_article = {'raw_text': ''}
            
            current_article['raw_text'] = current_article.get('raw_text', '') + line + '\n'
            
            if line.startswith('TI  - '):
                current_article['title'] = line[6:]
            elif line.startswith('AB  - '):
                current_article['abstract'] = line[6:]
            elif line.startswith('AU  - '):
                current_article.setdefault('authors', []).append(line[6:])
            elif line.startswith('PY  - '):
                current_article['year'] = line[6:]
            elif line.startswith('T2  - '):
                current_article['journal'] = line[6:]
            elif line.startswith('N1  - '):
                match = re.search(r'Cited By: (\d+)', line)
                if match:
                    current_article['citations'] = int(match.group(1))
                else:
                    current_article['citations'] = 0

    if current_article:
        articles.append(current_article)
    return articles

def score_article(article):
    score = 0
    text = (article.get('title', '') + ' ' + article.get('abstract', '')).lower()
    
    # Critical: Multilevel (The class requirement)
    if any(x in text for x in ['multilevel', 'multi-level', 'hierarchical linear', 'nested model', 'multilevel model']):
        score += 10
    elif 'hierarchical' in text: # Weaker signal
        score += 5
        
    # Critical: Mixed Methods
    if 'mixed method' in text:
        score += 10
    elif 'qualitative' in text and 'quantitative' in text:
        score += 5
        
    # Topic: VBHC
    if any(x in text for x in ['vbhc', 'value-based', 'value based']):
        score += 5
        
    # Context: Portugal/NHS
    if any(x in text for x in ['portugal', 'portuguese']):
        score += 5
    elif 'nhs' in text or 'national health service' in text:
        score += 3
        
    # Citations (small boost)
    score += min(article.get('citations', 0), 10) * 0.5
    
    return score

def main():
    file_path = r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\scopus.ris'
    articles = parse_ris(file_path)
    
    # Score and sort
    for art in articles:
        art['score'] = score_article(art)
        
    sorted_articles = sorted(articles, key=lambda x: x['score'], reverse=True)
    
    # Output top 10 to file
    with open(r'\\wsl.localhost\Ubuntu\home\dpolonia\202511-AMMMA\Docs\03_top_10_articles.md', 'w', encoding='utf-8') as f:
        f.write(f"# Top 10 Articles Analysis\n\n")
        for i, art in enumerate(sorted_articles[:10], 1):
            f.write(f"## {i}. {art.get('title', 'No Title')}\n")
            f.write(f"**Score:** {art['score']} | **Citations:** {art.get('citations', 0)} | **Year:** {art.get('year', 'N/A')}\n")
            f.write(f"**Journal:** {art.get('journal', 'N/A')}\n")
            f.write(f"**Authors:** {', '.join(art.get('authors', [])[:3])} et al.\n")
            f.write(f"**Abstract Snippet:** {art.get('abstract', '')[:300]}...\n\n")

if __name__ == "__main__":
    main()
