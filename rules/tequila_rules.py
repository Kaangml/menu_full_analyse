from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_tequila(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    tequila_keywords = ["tequila", "tekila", "mezcal"]
    shot_keywords = ["shot", "5+1", "6li", "4+1", "10pack", "fullpack"]

    # Öncelik Tekila
    if any(k in cat_n for k in tequila_keywords) or any(k in name_n for k in tequila_keywords):
        return "Tekila"

    # Tekila değilse Shot kontrolü
    if any(k in name_n for k in shot_keywords):
        return "Shot"

    return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti
# ---------------------------
# def detect_tequila_sub(name, category=None):
#     name_n = normalize(name)
#     shot_keywords = ["shot", "5+1", "6li", "4+1", "10pack", "fullpack"]
#     if any(k in name_n for k in shot_keywords):
#         return "Shot"
#     return None
