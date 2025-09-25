from rules.common import normalize

# Vodka anahtar kelimeleri
VODKA_KEYWORDS = [
    "vodka", "votka", "absolut", "smirnoff", "belvedere", "beluga", "russian standard",
    "finlandia", "grey goose", "ciroc", "titos", "haku", "ketel one", "gilbey", "zubrowka",
    "binboa", "mont blanc", "kastra elion", "koskenkorva", "onegin", "kauffman", "pravda",
    "wulf", "puschkin", "altamura", "avantgarde", "no:2"
]

def detect_vodka(name, category=None):
    """
    Vodka ana kategori tespiti
    """
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""
    all_vodka = [normalize(k) for k in VODKA_KEYWORDS]

    if any(k in name_n for k in all_vodka):
        return True
    if any(k in cat_n for k in ["vodka", "votka"]):
        return True
    return False