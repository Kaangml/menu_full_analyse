from rules.common import normalize

# ---------------------------
# Ana kategori tespiti
# ---------------------------
def detect_raki(name, category=None):
    name_n = normalize(name)
    cat_n = normalize(category) if category else ""

    # Ana kategori kontrolü
    if any(k in name_n for k in ["raki", "rakı","yenirak","rak"]) or any(k in cat_n for k in ["raki", "rakı","rak","yenirak"]):
        main_cat = "Rakı"
    else:
        return False  # Ana kategori değilse False döndür

# ---------------------------
# Alt kategori tespiti
# ---------------------------
def detect_raki_sub(name, category=None):
    name_n = normalize(name)

    if any(k in name_n for k in ["yeniraki", "yeni seri", "yeni raki 1937", "yeni raki ala", "yeni raki giz"]):
        return "Yeni Rakı"

    if any(k in name_n for k in ["tekirdag", "tekirdag rakisi", "tekirdag gold", "tekirdag altin seri"]):
        return "Tekirdağ Rakısı"

    if any(k in name_n for k in ["beylerbeyi", "b.gobek", "b.mavi", "b.kalecik", "b.teragold", "b.incir"]):
        return "Beylerbeyi Rakısı"

    if any(k in name_n for k in ["efe", "efe gold", "efe yesil", "efe yas uzum"]):
        return "Efe Rakısı"

    if any(k in name_n for k in ["kulup", "altinbas", "prototip", "protopi", "sari zeybek", "saki", "mercan", "ouzo of plomari"]):
        return "Özel Rakılar"

    return "Diğer / Özel Tipler"
