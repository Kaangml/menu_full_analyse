import re
from rules.common import normalize,compile_patterns
from collections import OrderedDict
import pandas as pd

# ---------- Ana kategori kuralları ----------
ANA_PATTERNS = {
    "Draft Beer": ["draft","draught","tap","fici","fıçı"],
    "Bottle Beer": ["bottle","bottled","şişe","kutu","can"],
    "Craft Beer": ["craft"],
    "World Beer": ["world","import","belgian","german"],
    "Cider": ["cider","apple cider","pear cider"],
    "Non-Alcoholic": ["alkolsuz","0.0","alcohol free"],
    "Combo / Menü": ["kombinasyon","paket","set","menü","menu","bundle"],
    "Yemek / Snack": ["snack","atıştırmalık","yemek","meze","mutfak"]
}

PRIORITY_ORDER = ["Combo / Menü","Draft Beer","Bottle Beer","Craft Beer","World Beer","Cider","Non-Alcoholic","Yemek / Snack"]

# ---------- Stil kuralları ----------
beer_styles = OrderedDict({
    "IPA": ["belgian ipa","american ipa","rye ipa","fruit ipa","wheat ipa","neipa","session ipa","ddh ipa","ipa"],
    "Pilsner": ["italian pilsener","pilsener","pilsner"],
    "Lager": ["dry hopped lager","unfiltered lager","vienna lager","munich lager","munich helles","helles","lager"],
    "Stout/Porter": ["stout & porter","imperial stout","oatmeal stout","milk stout","irish stout","porter","stout"],
    "Weiss/Wheat": ["weizenbock","wheat beer","wheat","weissbier","weisse bira","weisse","weiss","witbier","fruity wheat"],
    "Ale": ["hoppy blonde ale","amber ale","blonde ale","red ale","golden ale","pale ale","farmhouse ale","bitter ale","vintage ale","ale"],
    "Tripel": ["belgian tripel","tripel ale","tripel"],
    "Quadrupel": ["quadrupel"],
    "Saison": ["saison"],
    "Sour": ["fruited sour","fruity sour","sour"],
    "Fruity": ["fruit beer","fruited ipa","fruity ale"],
    "Smoked": ["smoked"],
})
# ---------- Segment mapping ----------
SEGMENT_MAP = {
    "EFES": "Core",
    "BOMONTI": "UMS",
    "MARMARA": "Core",
    "HEINEKEN": "UMS",
    "CARLSBERG": "Premium",
    "BUD": "UMS",
    "BUDWEISER": "UMS",
    "MILLER": "UMS",
    "BECK": "UMS",
    "SOL": "UMS",
    "AMSTEL": "UMS",
    "KNIDOS": "UMS",
    "TUBORG": "Premium",
    "FREDERIK": "Premium",
    "CORONA": "Premium",
    "GRIMBERGEN": "Premium",
    "ERDINGER": "Premium",
    "PAULANER": "Premium",
    "HOEGAARDEN": "Premium",
    "BELFAST": "Premium",
    "WEIHENSTEPHAN": "Premium",
    "KRONENBOURG": "Premium",
    "1664": "Premium",
    "GUINNESS": "Premium",
    "DUVEL": "Premium",
    "LEFFE": "Premium",
    "GARA": "Premium",
    "BREWDOG": "Premium",
    "CHIMAY": "Premium",
    "DELIRIUM": "Premium",
    "AMSTERDAM": "Yüksek Alkol",
    "GOLDEN": "Yüksek Alkol",
    "STRONG": "Yüksek Alkol",
    "GUINNESS FOREIGN": "Yüksek Alkol"
}

# ---------- Fonksiyonlar ----------
def detect_beer(name, category):
    name_n, cat_n = normalize(name), normalize(category)
    return any(k in name_n for k in ["beer","bira","fici","fıçı","draught","draft"]) \
        or any(k in cat_n for k in ["beer","bira","fici","fıçı","draught","draft"])

def detect_beer_sub(name, category):
    name_n, cat_n = normalize(name), normalize(category)
    for label in PRIORITY_ORDER:
        if any(k in name_n for k in ANA_PATTERNS[label]) or any(k in cat_n for k in ANA_PATTERNS[label]):
            return label
    return "Other"

style_pat_map = OrderedDict((k, compile_patterns(v)) for k,v in beer_styles.items())

def first_match_label(texts, label_to_patterns):
    for label, patterns in label_to_patterns.items():
        for t in texts:
            if any(p.search(t) for p in patterns):
                return label
    return None

def detect_style(row):
    """
    Gelişmiş Bira Stili tespiti:
    - Kendi içinde normalize eder.
    - Category → Product Name → İçerik sırasına göre eşleşme kontrolü.
    - Hiç eşleşme yoksa 'Genel' döner.
    """

    if row.get("Ana Kategori") != "Bira":
        return None
    # Normalize
    cat = normalize(row.get("Category", ""))
    pn  = normalize(row.get("Product Name", ""))
    ic  = normalize(row.get("İçerik", ""))

    # Category
    lab = first_match_label([cat], style_pat_map)
    if lab:
        return lab
    # Product Name
    lab = first_match_label([pn], style_pat_map)
    if lab:
        return lab
    # İçerik
    lab = first_match_label([ic], style_pat_map)
    if lab:
        return lab
    return "Genel"


def detect_beer_segment(name):
    name_upper = str(name).upper()
    for brand, seg in SEGMENT_MAP.items():
        if brand in name_upper:
            return seg
    return "Diğer/Belirsiz"

def extract_package(name, category):
    txt = f"{name} {category}".lower()  # name + category birleşimi
    if any(k in txt for k in ["draft","fıçı","draught","tap","fici"]):
        return "Fıçı"
    if any(k in txt for k in ["kutu","can"]):
        return "Kutu"
    if any(k in txt for k in ["şişe","bottle"]):
        return "Şişe"
    return "Diğer"