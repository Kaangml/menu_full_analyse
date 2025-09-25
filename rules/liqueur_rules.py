from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_liqueur(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Category kontrolü
    if any(k in cat_n for k in ["likor", "liqueur", "liqour", "cream", "creme"]):
        return "Likör"

    # Bilinen marka kontrolü
    known_brands = [
        "baileys", "malibu", "kahlua", "bakersfield", "limoncello",
        "passoa", "ramazotti", "cardinalmelon", "safari", "archers",
        "chambord", "amarula", "amaretto", "drambuie", "triplesec",
        "jagermeister", "aperol", "cointreau", "campari", "stgermain",
        "luxardo", "sheridans", "bumbucream", "disaronno"
    ]
    if any(b in name_n for b in known_brands):
        return "Likör"

    return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti (isteğe göre geliştirilebilir)
# ---------------------------
# def detect_liqueur_sub(name, category=None):
#     name_n = normalize(name)

#     # Örnek alt kategoriler
#     if any(b in name_n for b in ["baileys", "malibu", "bumbucream"]):
#         return "Krem Likör"
#     if any(b in name_n for b in ["limoncello", "triplesec", "cointreau", "campari"]):
#         return "Citrus / Likör"
#     if any(b in name_n for b in ["amarula", "amarula"]):
#         return "Afrika Likörü"

#     return "Diğer / Özel Tipler"
