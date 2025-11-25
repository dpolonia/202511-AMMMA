"""
Phase 3: Paper Selection & Retrieval
Present top papers, allow user selection, and download/extract paper.
"""

import json
import requests
from pathlib import Path
from typing import Dict, Optional
import config
import utils
import os

def display_top_papers(graded_papers: list, num_papers: int = 20):
    """Display top N papers for user selection."""
    print("\n" + "="*60)
    print(f"TOP {num_papers} PAPERS")
    print("="*60)
    
    for i, paper in enumerate(graded_papers[:num_papers], 1):
        grading = paper['grading']
        print(f"\n{i}. {paper['title']}")
        print(f"   Score: {grading['total_score']}/100")
        print(f"   Authors: {paper['authors']}")
        print(f"   Journal: {paper['publication_name']}")
        print(f"   Year: {paper['cover_date'][:4] if paper['cover_date'] != 'N/A' else 'N/A'}")
        print(f"   Citations: {paper['cited_by_count']}")
        print(f"   DOI: {paper['doi']}")

def select_paper(graded_papers: list) -> Dict:
    """Interactive paper selection."""
    while True:
        try:
            choice = int(utils.get_user_input(f"\nSelect paper number (1-{min(20, len(graded_papers))}): ").strip())
            if 1 <= choice <= min(20, len(graded_papers)):
                return graded_papers[choice - 1]
            print(f"Please enter a number between 1 and {min(20, len(graded_papers))}")
        except ValueError:
            print("Please enter a valid number")

def download_from_scopus(paper: Dict) -> Optional[Path]:
    """Attempt to download PDF from Scopus."""
    scopus_id = paper.get('scopus_id')
    if not scopus_id:
        return None
    
    headers = {
        'X-ELS-APIKey': config.SCOPUS_API_KEY,
        'Accept': 'application/pdf'
    }
    
    try:
        url = f"https://api.elsevier.com/content/article/scopus_id/{scopus_id}"
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
            pdf_path = config.SELECTED_PAPER_DIR / f"{scopus_id}.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded from Scopus")
            return pdf_path
    except Exception as e:
        print(f"✗ Scopus download failed: {e}")
    
    return None

def download_from_doi(doi: str) -> Optional[Path]:
    """Attempt to download PDF via DOI resolution."""
    if doi == 'N/A':
        return None
    
    try:
        # Try DOI.org redirect
        response = requests.get(f"https://doi.org/{doi}", allow_redirects=True, timeout=30)
        
        if response.status_code == 200 and 'application/pdf' in response.headers.get('content-type', ''):
            pdf_path = config.SELECTED_PAPER_DIR / f"{doi.replace('/', '_')}.pdf"
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded via DOI")
            return pdf_path
    except Exception as e:
        print(f"✗ DOI download failed: {e}")
    
    return None

def download_from_unpaywall(doi: str) -> Optional[Path]:
    """Attempt to download from Unpaywall (open access)."""
    if doi == 'N/A':
        return None
    
    try:
        # Unpaywall API
        email = "research@example.com"  # Replace with actual email
        url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            oa_location = data.get('best_oa_location')
            
            if oa_location and oa_location.get('url_for_pdf'):
                pdf_url = oa_location['url_for_pdf']
                pdf_response = requests.get(pdf_url, timeout=30)
                
                if pdf_response.status_code == 200:
                    pdf_path = config.SELECTED_PAPER_DIR / f"{doi.replace('/', '_')}.pdf"
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
                    print(f"✓ Downloaded from Unpaywall (Open Access)")
                    return pdf_path
    except Exception as e:
        print(f"✗ Unpaywall download failed: {e}")
    
    return None

def manual_upload_prompt(paper: Dict) -> Optional[Path]:
    """Prompt user to manually upload PDF."""
    print("\n" + "="*60)
    print("MANUAL PDF UPLOAD REQUIRED")
    print("="*60)
    print("\nAutomatic download failed. Please manually download the paper:")
    print(f"\nTitle: {paper['title']}")
    print(f"DOI: {paper['doi']}")
    print(f"\nSuggested sources:")
    print(f"  1. https://doi.org/{paper['doi']}")
    print(f"  2. Google Scholar: https://scholar.google.com/scholar?q={paper['title'].replace(' ', '+')}")
    print(f"  3. Publisher website")
    print(f"\nPlease save the PDF to: {config.SELECTED_PAPER_DIR}")
    print(f"Filename: paper.pdf")
    
    # Ensure directory exists
    config.SELECTED_PAPER_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check for demo PDF injection
    demo_pdf = os.getenv("AMMMA_DEMO_PDF_PATH")
    if demo_pdf and os.path.exists(demo_pdf):
        print(f"\n[DEMO MODE] Injecting PDF from: {demo_pdf}")
        import shutil
        target_path = config.SELECTED_PAPER_DIR / "paper.pdf"
        try:
            shutil.copy2(demo_pdf, target_path)
            print("✓ PDF injected successfully")
            return target_path
        except Exception as e:
            print(f"✗ Failed to inject demo PDF: {e}")
            
    utils.get_user_input("\nPress Enter once you've placed the PDF in the folder...")
    
    # Check if file exists
    pdf_path = config.SELECTED_PAPER_DIR / "paper.pdf"
    if pdf_path.exists():
        print("✓ PDF found!")
        return pdf_path
    else:
        print("✗ PDF not found. Please try again.")
        return None

def download_paper(paper: Dict) -> Optional[Path]:
    """
    Attempt to download paper using multiple methods.
    Falls back to manual upload if all fail.
    """
    print("\n" + "="*60)
    print("DOWNLOADING PAPER")
    print("="*60)
    
    # Method 1: Scopus
    print("\n[1/3] Attempting Scopus download...")
    pdf_path = download_from_scopus(paper)
    if pdf_path:
        return pdf_path
    
    # Method 2: DOI
    print("\n[2/3] Attempting DOI resolution...")
    pdf_path = download_from_doi(paper['doi'])
    if pdf_path:
        return pdf_path
    
    # Method 3: Unpaywall
    print("\n[3/3] Attempting Unpaywall (Open Access)...")
    pdf_path = download_from_unpaywall(paper['doi'])
    if pdf_path:
        return pdf_path
    
    # Fallback: Manual upload
    print("\n✗ All automatic download methods failed")
    pdf_path = manual_upload_prompt(paper)
    
    return pdf_path

def extract_paper_text(pdf_path: Path) -> str:
    """Extract text from PDF."""
    print("\n" + "="*60)
    print("EXTRACTING TEXT FROM PDF")
    print("="*60)
    
    text = utils.extract_pdf_text(pdf_path)
    
    if text:
        text_path = config.SELECTED_PAPER_DIR / "paper_text.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ Text extracted: {len(text)} characters")
        print(f"✓ Saved to: {text_path}")
        return text
    else:
        print("✗ Failed to extract text from PDF")
        return ""

def get_cited_papers(scopus_id: str) -> list:
    """Get papers cited by the selected paper (references)."""
    if not scopus_id:
        return []
    
    headers = {
        'X-ELS-APIKey': config.SCOPUS_API_KEY,
        'Accept': 'application/json'
    }
    
    try:
        # Get abstract which contains references
        url = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"
        params = {'view': 'REF'}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            refs = data.get('abstracts-retrieval-response', {}).get('references', {}).get('reference', [])
            
            cited_papers = []
            for ref in refs[:10]:  # Limit to first 10 references
                ref_info = ref.get('ref-info', {})
                cited_papers.append({
                    'title': ref_info.get('ref-title', {}).get('ref-titletext', 'N/A'),
                    'doi': ref_info.get('refd-itemidlist', {}).get('itemid', [{}])[0].get('$', 'N/A'),
                    'scopus_id': ref.get('scopus-id', 'N/A')
                })
            
            return cited_papers
    except Exception as e:
        print(f"✗ Error fetching cited papers: {e}")
    
    return []

def get_citing_papers(scopus_id: str) -> list:
    """Get papers that cite the selected paper."""
    if not scopus_id:
        return []
    
    headers = {
        'X-ELS-APIKey': config.SCOPUS_API_KEY,
        'Accept': 'application/json'
    }
    
    try:
        # Search for papers citing this one
        query = f"REF({scopus_id})"
        url = config.SCOPUS_SEARCH_URL
        params = {
            'query': query,
            'count': 10  # Limit to 10 citing papers
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])
            
            citing_papers = []
            for entry in entries:
                citing_papers.append({
                    'title': entry.get('dc:title', 'N/A'),
                    'doi': entry.get('prism:doi', 'N/A'),
                    'scopus_id': entry.get('dc:identifier', '').replace('SCOPUS_ID:', '')
                })
            
            return citing_papers
    except Exception as e:
        print(f"✗ Error fetching citing papers: {e}")
    
    return []

def download_related_papers(paper: Dict):
    """Download PDFs of cited and citing papers if available."""
    print("\n" + "="*60)
    print("DOWNLOADING RELATED PAPERS")
    print("="*60)
    
    scopus_id = paper.get('scopus_id')
    
    # Create subdirectories
    cited_dir = config.SELECTED_PAPER_DIR / "cited_papers"
    citing_dir = config.SELECTED_PAPER_DIR / "citing_papers"
    cited_dir.mkdir(exist_ok=True)
    citing_dir.mkdir(exist_ok=True)
    
    # Get cited papers (references)
    print("\n[1/2] Fetching cited papers (references)...")
    cited_papers = get_cited_papers(scopus_id)
    print(f"Found {len(cited_papers)} cited papers")
    
    cited_count = 0
    for i, cited in enumerate(cited_papers, 1):
        print(f"\n  [{i}/{len(cited_papers)}] {cited['title'][:60]}...")
        
        # Try to download
        pdf_path = None
        if cited['doi'] != 'N/A':
            pdf_path = download_from_unpaywall(cited['doi'])
            if pdf_path:
                # Move to cited_papers directory
                new_path = cited_dir / f"cited_{i}_{cited['doi'].replace('/', '_')}.pdf"
                pdf_path.rename(new_path)
                cited_count += 1
                print(f"    ✓ Downloaded")
    
    print(f"\n✓ Downloaded {cited_count}/{len(cited_papers)} cited papers")
    
    # Get citing papers
    print("\n[2/2] Fetching citing papers...")
    citing_papers = get_citing_papers(scopus_id)
    print(f"Found {len(citing_papers)} citing papers")
    
    citing_count = 0
    for i, citing in enumerate(citing_papers, 1):
        print(f"\n  [{i}/{len(citing_papers)}] {citing['title'][:60]}...")
        
        # Try to download
        pdf_path = None
        if citing['doi'] != 'N/A':
            pdf_path = download_from_unpaywall(citing['doi'])
            if pdf_path:
                # Move to citing_papers directory
                new_path = citing_dir / f"citing_{i}_{citing['doi'].replace('/', '_')}.pdf"
                pdf_path.rename(new_path)
                citing_count += 1
                print(f"    ✓ Downloaded")
    
    print(f"\n✓ Downloaded {citing_count}/{len(citing_papers)} citing papers")
    
    # Save metadata
    related_metadata = {
        'cited_papers': cited_papers,
        'citing_papers': citing_papers,
        'cited_downloaded': cited_count,
        'citing_downloaded': citing_count
    }
    
    metadata_path = config.SELECTED_PAPER_DIR / "related_papers_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(related_metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Related papers metadata saved to: {metadata_path.name}")
    
    return related_metadata

def save_paper_metadata(paper: Dict):
    """Save selected paper metadata."""
    metadata_path = config.SELECTED_PAPER_DIR / "paper_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(paper, f, indent=2, ensure_ascii=False)
    print(f"✓ Metadata saved to: {metadata_path}")

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 3: PAPER SELECTION & RETRIEVAL")
    print("="*60)
    
    # Load graded papers
    try:
        graded_papers = utils.load_json(config.OUTPUT_FILES['graded_papers'])
    except FileNotFoundError:
        print("\n❌ ERROR: graded_papers.json not found!")
        print("Please run Phase 2 (02_grading_algorithm.py) first.")
        return False
    
    # Display top papers
    display_top_papers(graded_papers, 20)
    
    # User selects paper
    selected_paper = select_paper(graded_papers)
    
    print("\n" + "="*60)
    print("SELECTED PAPER")
    print("="*60)
    print(f"\nTitle: {selected_paper['title']}")
    print(f"Score: {selected_paper['grading']['total_score']}/100")
    print(f"DOI: {selected_paper['doi']}")
    
    # Download paper
    pdf_path = download_paper(selected_paper)
    
    if not pdf_path:
        print("\n❌ Failed to obtain PDF. Please try again.")
        return False
    
    # Extract text
    text = extract_paper_text(pdf_path)
    
    if not text:
        print("\n⚠ Warning: Text extraction failed, but PDF is available")
    
    # Save metadata
    save_paper_metadata(selected_paper)
    
    # Download related papers (cited and citing)
    related_metadata = download_related_papers(selected_paper)
    
    print("\n" + "="*60)
    print("✓ PHASE 3 COMPLETE")
    print("="*60)
    print(f"\nPaper saved to: {config.SELECTED_PAPER_DIR}")
    print(f"PDF: {pdf_path.name}")
    if text:
        print(f"Text: paper_text.txt ({len(text)} characters)")
    print(f"Metadata: paper_metadata.json")
    print(f"\nRelated Papers:")
    print(f"  Cited papers: {related_metadata['cited_downloaded']}/{len(related_metadata['cited_papers'])} downloaded")
    print(f"  Citing papers: {related_metadata['citing_downloaded']}/{len(related_metadata['citing_papers'])} downloaded")
    print("\nYou can now proceed to Phase 4 (Evaluation Answering)")
    
    return True

if __name__ == "__main__":
    main()
