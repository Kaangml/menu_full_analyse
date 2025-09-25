from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_cocktail(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    if any(k in cat_n for k in ["alkolsuz", "non-alcoholic"]):
        return "Alkolsüz Kokteyl"
    
    if any(k in cat_n for k in ["kokteyl", "cocktail", "imza", "signature"]):
        return "Kokteyl"

    return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti
# ---------------------------
def detect_cocktail_sub(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Category bazlı öncelik
    if any(k in cat_n for k in ["klasik", "classic"]):
        return "Klasik / Classic Kokteyl"
    if any(k in cat_n for k in ["signature", "imza", "house", "ozel", "special", "publique"]):
        return "Signature / Özel / House Kokteyl"
    if any(k in cat_n for k in ["alkolsuz", "non-alcoholic"]):
        return "Alkolsüz Kokteyl / Non-Alcoholic"
    if any(k in cat_n for k in ["world", "global", "evrensel"]):
        return "Global / World / Evrensel Kokteyl"

    # Name bazlı kontrol
    classic_cocktails = [
        "cuba libre", "negroni", "margarita", "mojito", "long island", 
        "tequila sunrise", "sex on the beach", "blue hawaii", 
        "lynburg lemonade", "lcynburg lemonade", "blue apple", "red margarita", "gin fizz"
    ]
    if any(k in name_n for k in classic_cocktails):
        return "Klasik / Classic Kokteyl"

    signature_keywords = ["signature", "imza", "house", "ozel", "special", "publique"]
    if any(k in name_n for k in signature_keywords):
        return "Signature / Özel / House Kokteyl"

    if any(k in name_n for k in ["alkolsuz", "non-alcoholic"]):
        return "Alkolsüz Kokteyl / Non-Alcoholic"

    if any(k in name_n for k in ["world", "global", "evrensel"]):
        return "Global / World / Evrensel Kokteyl"

    return "Diğer / Özel Tipler"
