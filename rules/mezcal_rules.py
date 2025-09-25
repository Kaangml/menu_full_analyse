import pandas as pd
from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_mezcal(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    mezcal_keywords = ["mezcal", "casamigos", "oaxaca", "del maguey", "illegal", "ojedetigre"]
    shot_keywords = ["shot", "5+1", "6li", "4+1", "10pack", "fullpack"]
    vermut_keywords = ["vermut", "vermouth", "martini", "garrone", "campari", "ramazotti", "martell"]

    if any(k in cat_n for k in mezcal_keywords) or any(k in name_n for k in mezcal_keywords):
        return "Mezcal"

    if any(k in name_n for k in shot_keywords):
        return "Shot"

    if any(k in cat_n for k in vermut_keywords) or any(k in name_n for k in vermut_keywords):
        return "Vermut"

    return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti
# ---------------------------
# def detect_mezcal_sub(name, category=None):
#     name_n = normalize(name)
#     shot_keywords = ["shot", "5+1", "6li", "4+1", "10pack", "fullpack"]
#     if any(k in name_n for k in shot_keywords):
#         return "Shot"
#     return None
