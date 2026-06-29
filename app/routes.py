from flask import render_template, request, jsonify
from app import app
import joblib
import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import warnings
warnings.filterwarnings('ignore')

# Load models and explainers
rf_url_only = joblib.load('model/url_only_model.pkl')
rf_hybrid = joblib.load('model/hybrid_model.pkl')

with open('model/shap_explainer_url.pkl', 'rb') as f:
    explainer_url = pickle.load(f)

with open('model/shap_explainer_hybrid.pkl', 'rb') as f:
    explainer_hybrid = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'})
    
    # Extract URL features
    from src.url_features import extract_url_features
    url_feats = extract_url_features(url)
    url_df = pd.DataFrame([url_feats])

    # URL-only prediction
    url_pred = rf_url_only.predict(url_df)[0]
    url_prob = rf_url_only.predict_proba(url_df)[0][1]
    
    # URL SHAP explanation
    url_shap = explainer_url.shap_values(url_df)
    url_shap_vals = url_shap[:, :, 1][0]
    url_shap_dict = dict(zip(url_df.columns, [round(float(v), 4) for v in url_shap_vals]))
    top_url_features = sorted(url_shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    
    # Try HTML features
    from src.html_features import extract_html_features
    html_feats = extract_html_features(url)
    html_fetched = html_feats.get('fetch_status', 0)
    
    hybrid_pred = None
    hybrid_prob = None
    top_hybrid_features = None
    
    if html_fetched:
        combined_feats = {**url_feats, **html_feats}
        combined_feats.pop('fetch_status', None)
        combined_df = pd.DataFrame([combined_feats])
        
        hybrid_pred = rf_hybrid.predict(combined_df)[0]
        hybrid_prob = rf_hybrid.predict_proba(combined_df)[0][1]
        
        hybrid_shap = explainer_hybrid.shap_values(combined_df)
        hybrid_shap_vals = hybrid_shap[:, :, 1][0]
        hybrid_shap_dict = dict(zip(combined_df.columns, [round(float(v), 4) for v in hybrid_shap_vals]))
        top_hybrid_features = sorted(hybrid_shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
    
    return jsonify({
        'url': url,
        'url_only': {
            'prediction': int(url_pred),
            'probability': round(float(url_prob), 4),
            'top_features': top_url_features
        },
        'hybrid': {
            'prediction': int(hybrid_pred) if hybrid_pred is not None else None,
            'probability': round(float(hybrid_prob), 4) if hybrid_prob is not None else None,
            'top_features': top_hybrid_features,
            'html_fetched': bool(html_fetched)
        }
    })