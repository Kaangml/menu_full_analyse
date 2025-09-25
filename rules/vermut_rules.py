from rules.common import normalize

def detect_vermut(text):
    t = normalize(text)
    if "vermut" in t or "vermouth" in t:
        return "Vermut"
    return None
