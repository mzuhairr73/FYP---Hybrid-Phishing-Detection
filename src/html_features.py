import requests
import re
from bs4 import BeautifulSoup

def extract_html_features(url):
    features = {}
    
    url = str(url)
    if not url.startswith('http'):
        url = 'http://' + url
    
    try:
        response = requests.get(url, timeout=5, verify=False,
                                headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        
        features['num_iframes'] = len(soup.find_all('iframe'))
        features['num_scripts'] = len(soup.find_all('script'))
        features['num_images'] = len(soup.find_all('img'))
        features['num_links'] = len(soup.find_all('a'))
        features['num_forms'] = len(soup.find_all('form'))
        features['num_inputs'] = len(soup.find_all('input'))
        
        password_inputs = soup.find_all('input', {'type': 'password'})
        features['has_password_field'] = 1 if len(password_inputs) > 0 else 0
        
        scripts = soup.find_all('script', src=True)
        features['num_external_scripts'] = sum(
            1 for s in scripts if s['src'].startswith('http')
        )
        
        imgs = soup.find_all('img', src=True)
        features['num_external_images'] = sum(
            1 for i in imgs if i['src'].startswith('http')
        )
        
        hidden = soup.find_all(style=re.compile(r'display\s*:\s*none'))
        features['num_hidden_elements'] = len(hidden)
        
        features['page_size'] = len(response.content)
        features['fetch_status'] = 1
        
    except:
        features = {
            'num_iframes': 0, 'num_scripts': 0, 'num_images': 0,
            'num_links': 0, 'num_forms': 0, 'num_inputs': 0,
            'has_password_field': 0, 'num_external_scripts': 0,
            'num_external_images': 0, 'num_hidden_elements': 0,
            'page_size': 0, 'fetch_status': 0
        }
    
    return features