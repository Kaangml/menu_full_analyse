import re
from rules.common import normalize

# ---------------------------
# WHISKY KEYWORDS
# ---------------------------

# Ana kategori kelimeleri
WHISKY_KEYWORDS = [
    "whisky", "whiskey", "viski", "label", "single malt", "bourbon", "rye",
    "Viskı", "İTHAL ALKOL / VİSKİ"
]

# Alt kategori listeleri
BLENDED = ["johnnie walker", "chivas", "ballantine", "famous grouse", "j&b", "dewars"]
SINGLE_MALT = [
    "glenfiddich", "glenlivet", "macallan", "lagavulin", "talisker", "laphroaig",
    "highland park", "bowmore", "aberlour", "ardbeg", "caol ila", "cardhu",
    "balvenie", "singleton", "kavalan", "paul john", "oban", "glenkinchie",
    "glenfarclas", "dalmore", "glenmoray", "tamnavulin", "clynelish", "kilchoman",
    "jura", "bruichladdich", "hakashu", "starward", "amrut", "yoichi",
    "miyagikyo", "scapa", "the chita", "smokey monkey", "royal salute"
]
IRISH = ["jameson", "bushmills", "teeling", "powers", "redbreast", "hyde"]
BOURBON = ["jack daniel", "maker's mark", "wild turkey", "woodford reserve",
           "jim beam", "bulleit", "lot40", "jb tek", "jp wiser"]
RYE = ["rye whiskey", "bulleit rye", "knob creek rye", "pike creek", "woodford rye"]
CANADIAN = ["canadian club", "crown royal", "forty creek", "lot 40"]
JAPANESE = ["nikka", "yamazaki", "hibiki", "hakushu", "kamiki", "togouchi", 
            "suntory toki", "yoichi", "miyagikyo"]

# Alt kategori mapping
SUB_RULES = {
    "Blended Whisky": BLENDED,
    "Single Malt": SINGLE_MALT,
    "Irish Whiskey": IRISH,
    "Bourbon": BOURBON,
    "Rye Whiskey": RYE,
    "Canadian Whisky": CANADIAN,
    "Japanese Whisky": JAPANESE
}

# ---------------------------
# FUNCTIONS
# ---------------------------

def detect_whisky(name, category):
    """Ana kategori: Viski mi değil mi?"""
    name_n = normalize(name)
    cat_n = normalize(category)
    
    all_keywords = [normalize(x) for x in WHISKY_KEYWORDS + BLENDED + SINGLE_MALT + IRISH + BOURBON + RYE + CANADIAN + JAPANESE]
    
    if any(k in name_n for k in all_keywords):
        return True
    whisky_indicators_in_cat = ["viski", "whisky", "whiskey", "scotch", "bourbon", "irish", "malt"]
    if any(k in cat_n for k in whisky_indicators_in_cat):
        return True
    return False

def detect_whisky_sub(name, category):
    """Alt kategori tespiti"""
    name_n = normalize(name)
    cat_n = normalize(category)
    
    for label, keywords in SUB_RULES.items():
        if any(normalize(x) in name_n for x in keywords):
            return label
    
    # Eğer isimden yakalanmadıysa Category kolonuna bak
    cat_mapping = {
        "blended": "Blended Whisky",
        "single malt": "Single Malt",
        "irish": "Irish Whiskey",
        "bourbon": "Bourbon",
        "rye": "Rye Whiskey",
        "canadian": "Canadian Whisky",
        "japanese": "Japanese Whisky",
        "scotch": "Blended/Single Malt Scotch",
        "malt": "Malt Whisky"
    }
    
    for key, val in cat_mapping.items():
        if key in cat_n:
            return val
    
    # Son çare
    if "whisky" in name_n or "whiskey" in name_n or "viski" in name_n:
        return "Other Whisky"
    
    return None
