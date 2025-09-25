from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_cognac(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Category kontrolü
    if any(k in cat_n for k in ["konyak", "brandy", "cognac"]):
        return "Konyak"
    
    # Bilinen marka kontrolü
    known_brands = ["martell", "hennessy", "remy martin", "courvoisier", "metaxa"]
    if any(b in name_n for b in known_brands):
        return "Konyak"

    return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti
# ---------------------------
def detect_cognac_sub(name, category=None):
    name_n = normalize(name)

    # Marka tespit
    brands = ["martell", "hennessy", "remy martin", "courvoisier", "metaxa"]
    brand_found = next((b.title() for b in brands if b in name_n), "Diğer / Özel Tipler")

    # Seri tespit
    series_patterns = ["vs", "vsop", "xo", "5 star", "excellence"]
    series_found = next((s.upper() for s in series_patterns if s in name_n), "")

    if series_found:
        return f"{brand_found} {series_found}"
    else:
        return brand_found
