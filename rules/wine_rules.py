from rules.common import normalize

# --- keyword listeleri ---
RED_WINE_KW = ["okuzgozu","bogazkere","kalecik","cabernet","merlot","syrah","pinotnoir","malbec","tempranillo","sangiovese"]
WHITE_WINE_KW = ["narince","emir","sultaniye","chardonnay","sauvignon","pinotgrigio","riesling","viognier"]
ROSE_WINE_KW = ["roze","rose","blush","pembe"]
SPARKLING_WINE_KW = ["kopuklu","kopuren","sparkling","champagne","prosecco","cava","cameo","moscato"]
BRAND_KW = ["buzbag","angora","doluca","kayra","kavaklidere","leona","itinera","vintage","kup"]

def detect_wine(name, category=None):
    """
    Ana kategori tespiti: Şarap mı değil mi
    """
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Üzüm/alt kategori kelimeleri
    if any(k in name_n for k in RED_WINE_KW + WHITE_WINE_KW + ROSE_WINE_KW + SPARKLING_WINE_KW):
        return True
    # Category kolonunda güvenli kelimeler
    if any(k in cat_n for k in ["sarap","wine","sparkling","kopuklu","kopuren","roze","aromali","meyve","likor"]):
        return True
    # Marka/etiket kelimeleri
    if any(k in name_n for k in BRAND_KW):
        return True
    return False

def detect_wine_sub(name, category=None):
    """
    Şarap alt kategorisi tespiti
    """
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    if any(k in name_n for k in RED_WINE_KW): return "Kırmızı Şarap"
    if any(k in name_n for k in WHITE_WINE_KW): return "Beyaz Şarap"
    if any(k in name_n for k in ROSE_WINE_KW): return "Roze / Blush"
    if any(k in name_n for k in SPARKLING_WINE_KW): return "Köpüklü & Premium Şarap"
    if any(k in cat_n for k in RED_WINE_KW): return "Kırmızı Şarap"
    if any(k in cat_n for k in WHITE_WINE_KW): return "Beyaz Şarap"
    if any(k in cat_n for k in ROSE_WINE_KW): return "Roze / Blush"
    if any(k in cat_n for k in SPARKLING_WINE_KW): return "Köpüklü & Premium Şarap"
    return "Other Wine"