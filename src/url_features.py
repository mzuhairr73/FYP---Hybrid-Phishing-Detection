import re
from urllib.parse import urlparse

def extract_url_features(url):
    features = {}
    
    url = str(url).strip()
    
    # Remove protocol to match training data format
    url_clean = url.replace('https://', '').replace('http://', '')
    
    try:
        parsed = urlparse(url if url.startswith('http') else 'http://' + url)
        domain = parsed.netloc
        path = parsed.path
    except:
        domain = ''
        path = ''
    
    # Use cleaned URL for length features to match training
    features['url_length'] = len(url_clean)
    features['domain_length'] = len(domain)
    features['path_length'] = len(path)
    
    # Count-based features on cleaned URL
    features['num_dots'] = url_clean.count('.')
    features['num_hyphens'] = url_clean.count('-')
    features['num_slashes'] = url_clean.count('/')
    features['num_at'] = url_clean.count('@')
    features['num_digits'] = sum(c.isdigit() for c in url_clean)
    features['num_params'] = url_clean.count('?')
    features['num_percent'] = url_clean.count('%')
    features['num_subdomains'] = len(domain.split('.')) - 2 if domain else 0
    
    # Binary features
    features['has_ip'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0
    features['has_https'] = 1 if url.startswith('https') else 0
    features['has_at_symbol'] = 1 if '@' in url_clean else 0
    features['has_double_slash'] = 1 if '//' in url_clean else 0
    
    # Suspicious keyword features
    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update',
                           'banking', 'confirm', 'password', 'signin', 'ebayisapi',
                           'webscr', 'cmd', 'dispatch', 'paypal']
    for keyword in suspicious_keywords:
        features[f'has_{keyword}'] = 1 if keyword in url_clean.lower() else 0
    
    return features