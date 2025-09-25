from rules.common import normalize

# --- Ana kategori tespiti ---
def detect_gin(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    if any(k in name_n for k in ["gin", "cin", "gin&", "gin-", "juniper"]) \
       or any(k in cat_n for k in ["gin", "cin", "gin&", "gin-", "juniper", "gintonic", 
                                   "gin kadeh", "gin şişe", "gin shot", "bottled gin"]):
        return True
    return False

# --- Alt kategori tespiti ---
def detect_gin_sub(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Aromalı Gin
    if any(k in name_n for k in ["pink","limon","lemon","rosa","bloodorange","sicilian","cilek","orange"]) \
       or "aromali" in cat_n:
        return "Aromalı Gin"

    # Premium / Craft Gin
    if any(k in name_n for k in ["monkey47","hendrick","roku","mare","botanist","knut","oxley","ashmont",
                                 "illusionist","mosaik","sipsmith","skagerrak","tanqueray10","no10",
                                 "seventyone","threebrothers"]):
        return "Premium / Craft Gin"

    # Classic Gin
    if "dry" in name_n or "londondry" in name_n or "classic" in name_n:
        return "Classic Gin"

    # Default
    return "Diğer Gin"
