# 🛡️ DocShield — Fake Document & Media Detector
## Django Python Website

### Features
- 📄 Document verification (Aadhaar, PAN, Marksheet, etc.)
- 🖼️ Deepfake photo detection
- 🎥 Fake video detection
- 📊 Scan history with detailed reports
- ⚡ AJAX-based instant results (page reload nahi hoti)

---

## 🚀 Kaise Run Karo

### Step 1 — Dependencies install karo
```bash
pip install -r requirements.txt
```

### Step 2 — Database setup karo
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3 — Server start karo
```bash
python manage.py runserver
```

### Step 4 — Browser mein open karo
```
http://127.0.0.1:8000/
```

---

## 📁 Project Structure
```
docshield/
├── manage.py
├── requirements.txt
├── docshield/          ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── detector/           ← Main app
    ├── models.py       ← ScanReport database model
    ├── views.py        ← Home, Analyze, History, Report views
    ├── urls.py         ← URL routing
    ├── analyzer.py     ← Detection logic (heuristic + ML ready)
    └── templates/
        └── detector/
            ├── base.html
            ├── home.html
            ├── history.html
            └── report_detail.html
```

---

## 🔬 Production ke liye ML Models Kaise Add Karo

`detector/analyzer.py` mein `analyze_file()` function ko upgrade karo:

```python
# Document forgery detection
from PIL import Image
import numpy as np
# ELA (Error Level Analysis) implement karo

# Deepfake detection
# FaceForensics++ model use karo
# pip install facenet-pytorch

# Video analysis  
# pip install opencv-python
```

---

## ⚠️ Disclaimer
Yeh educational tool hai. Legal document verification ke liye
official government portals aur authorities se confirm karo.
