from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_rum(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Category kontrolü
    if any(k in cat_n for k in ["rom", "rum", "cachaca", "cachaça"]):
        return "Rom"

    # Bilinen marka kontrolü
    known_brands = ["havana", "bacardi", "captain morgan", "bumbu", "diplomatico", "zacapa", "janeiro", "cachaca", "cachaça"]
    if any(b in name_n for b in known_brands):
        return "Rom"

    return False  # Ana kategori değilse False döndür

# # ---------------------------
# # Alt kategori tespiti
# # ---------------------------
# def detect_rum_sub(name, category=None):
#     name_n = normalize(name)
    
#     # Örnek alt kategoriler (isteğe göre genişletilebilir)
#     if any(b in name_n for b in ["havana", "bacardi", "captain morgan"]):
#         return "Karayip Romu"
#     if any(b in name_n for b in ["bumbu", "diplomatico", "zacapa"]):
#         return "Güney Amerika Romu"
#     if any(b in name_n for b in ["cachaca", "cachaça"]):
#         return "Brezilya Cachaca"
    
#     return "Diğer / Özel Tipler"
