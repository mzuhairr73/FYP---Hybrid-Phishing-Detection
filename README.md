# PhishLens — Hybrid Machine Learning for Phishing Website Detection

A final-year project that detects malicious URLs using a **hybrid machine-learning approach**, combining lexical features extracted from the URL with content features extracted from the live HTML of the page. Predictions are made explainable using **SHAP**, and served through a **Flask** web application.

## Overview

The system trains and compares two models:

- **URL-only model** — a Random Forest trained on 29 lexical features extracted from the URL string (length, character counts, subdomain structure, suspicious keywords, etc.).
- **Hybrid model** — a Random Forest trained on the URL features **plus** 11 content features fetched from the page's live HTML (script/link/iframe counts, form and password fields, external resources, page size, etc.).

Each prediction is accompanied by its top contributing features (via SHAP), and the web interface blends both models into a single threat score with a plain-language explanation of the decision.

## Tech stack

- Python 3.9+
- Flask (web application)
- scikit-learn (Random Forest models)
- pandas / numpy (data processing)
- BeautifulSoup + requests (HTML fetching and parsing)
- SHAP (explainability)
- joblib (model serialisation)

## Project structure

```
FYP project/
├── app/                  # Flask web application
│   ├── __init__.py
│   ├── routes.py         # Prediction endpoint and model loading
│   └── templates/
│       └── index.html    # Front-end UI
├── src/                  # Feature extraction logic
│   ├── url_features.py   # URL (lexical) feature extraction
│   └── html_features.py  # HTML (content) feature extraction
├── notebooks/            # Data exploration, training, explainability
│   ├── 01_eda.ipynb
│   ├── 02_feature_extraction.ipynb
│   ├── 03_html_features.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_explainability.ipynb
│   ├── 06_augment_benign.ipynb
│   └── 07_augment_hybrid.ipynb
├── model/                # Trained models (NOT in repo — see note below)
├── dataset/              # Datasets (NOT in repo — see note below)
├── requirements.txt
└── run.py                # Application entry point
```

## Note on model and dataset files

The `model/` and `dataset/` folders are **not included in this repository** because the trained models and CSV datasets are too large for GitHub. To run the application you need the `model/` folder, containing:

- `url_only_model.pkl`
- `hybrid_model.pkl`
- `shap_explainer_url.pkl`
- `shap_explainer_hybrid.pkl`

Copy this folder into the project root (so it sits alongside `run.py`) before running. The `dataset/` folder is only required if you intend to retrain the models from the notebooks.

## Setup and running

**1. Clone the repository**
```powershell
git clone https://github.com/mzuhairr73/FYP---Hybrid-Phishing-Detection.git
cd FYP---Hybrid-Phishing-Detection
```

**2. Create and activate a virtual environment**
```powershell
python -m venv venv
venv\Scripts\activate
```
If activation is blocked by an execution-policy error on Windows, run this once and then activate again:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**3. Install dependencies**
```powershell
pip install -r requirements.txt
```

**4. Add the model files**

Copy the `model/` folder (see note above) into the project root.

**5. Run the application**
```powershell
python run.py
```
Then open **http://127.0.0.1:5000** in a browser.

## Usage

Enter a URL (or click one of the example links) and the application will:

1. Extract lexical features from the URL and predict with the URL-only model.
2. Fetch the live page, extract HTML features, and predict with the hybrid model.
3. Display a blended threat score, each model's verdict and confidence, the top contributing features (SHAP), and a plain-language summary of the decision.

> The hybrid model requires internet access to fetch the target page. If a page cannot be reached (e.g. a taken-down phishing site), the application falls back to the URL-only verdict.

## Notes

- The dataset was simplified to binary classification: `benign` vs `malicious` (the latter covering phishing, defacement, and malware URLs).
- The benign class was augmented with legitimate domains from the Tranco top-sites list to address a bias against bare domains.
