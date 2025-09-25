from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_shot(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Category kontrolü
    if "shot" in cat_n:
        return "Shot"

    # Bilinen anahtar kelimeler
    shot_keywords = ["shot", "5+1", "6li", "4+1", "10pack", "fullpack"]
    if any(k in name_n for k in shot_keywords):
        return "Shot"

    return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti (opsiyonel)
# ---------------------------
# def detect_shot_sub(name, category=None):
#     name_n = normalize(name)

#     # Örnek alt kategoriler (isteğe göre geliştirilebilir)
#     if "5+1" in name_n or "6li" in name_n:
#         return "Mini Paket Shot"
#     if "10pack" in name_n or "fullpack" in name_n:
#         return "Büyük Paket Shot"

#     return "Diğer / Özel Tipler"
