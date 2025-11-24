import requests
import json

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

def test_serial(issn):
    base_url = "https://api.elsevier.com/content/serial/title"
    params = {
        'issn': issn,
        'view': 'STANDARD'
    }
    print(f"Testing ISSN: {issn}")
    try:
        response = requests.get(base_url, headers=HEADERS, params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            entry = data['serial-metadata-response']['entry'][0]
            print(f"SJR: {entry.get('SJRList', {}).get('SJR', [{}])[0].get('$', 'N/A')}")
            print(f"CiteScore: {entry.get('citeScoreYearInfoList', {}).get('citeScoreCurrentMetric', 'N/A')}")
            print(f"SNIP: {entry.get('SNIPList', {}).get('SNIP', [{}])[0].get('$', 'N/A')}")
        else:
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_serial("1422-8890") # Try with dash
    test_serial("14228890")  # Try without dash
