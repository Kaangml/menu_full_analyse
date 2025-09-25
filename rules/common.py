import re
import unicodedata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# HELPERS
# ---------------------------
def normalize(text):
    if pd.isna(text) or not text:
        return ""
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii","ignore").decode("utf-8")
    return re.sub(r'[^a-z0-9]', '', text.lower().strip())

def join_nonempty(parts, sep=" | "):
    parts = [p for p in parts if p and str(p).strip()]
    return sep.join(parts) if parts else ""

def compile_patterns(keys):
    keys_sorted = sorted(keys, key=len, reverse=True)
    return [re.compile(r"(?:^|[^a-z0-9ğüşöçı])" + re.escape(k) + r"(?:[^a-z0-9ğüşöçı]|$)") for k in keys_sorted]

def any_match(text, patterns):
    return any(p.search(text) for p in patterns)

def extract_volume(name, cl_value=None):
    name_lower = str(name).lower()
    match = re.search(r'(\d+)\s*(cl|ml)', name_lower)
    if match:
        return match.group(1) + match.group(2).upper()
    for word in ["kadeh","tek","single","duble","double","shot","şişe","kutu"]:
        if word in name_lower:
            return word.capitalize()
    if cl_value and pd.notna(cl_value):
        return str(cl_value).strip()
    return None


def normalize_brand(name):
    return " ".join(str(name).upper().split()[:3]) if name else ""

def clean_price_iqr_grouped(df, price_col="Price", group_cols=["Ana Kategori", "Hacim"], visualize=False):
    """
    Fiyat outlier temizliği (IQR yöntemi), grup bazlı (örn. kategori + hacim).
    
    Args:
        df (pd.DataFrame): Veri seti
        price_col (str): Fiyat kolonu
        group_cols (list): Gruplama kolonları (örn. kategori, hacim)
        visualize (bool): True -> her grup için grafik çizer

    Returns:
        pd.DataFrame: Temizlenmiş DataFrame
        dict: Grup bazlı istatistik bilgileri
    """
    df = df.copy()
    # Numerik fiyat çıkar
    df["_price_num"] = (
        df[price_col]
        .astype(str)
        .str.replace(r"[^\d,\.]", "", regex=True)
        .str.replace(",", ".", regex=False)
    )
    df["_price_num"] = pd.to_numeric(df["_price_num"], errors="coerce")

    stats_dict = {}
    clean_indices = []

    grouped = df.groupby(group_cols)
    for keys, group in grouped:
        prices = group["_price_num"].dropna()
        if len(prices) < 5:  # çok küçük grupları es geçelim
            clean_indices.extend(group.index.tolist())
            continue

        Q1 = prices.quantile(0.01)
        Q3 = prices.quantile(0.99)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        mask = (group["_price_num"] >= lower_bound) & (group["_price_num"] <= upper_bound)
        clean_indices.extend(group[mask].index.tolist())

        stats_dict[keys] = {
            "Q1": Q1, "Q3": Q3, "IQR": IQR,
            "lower_bound": lower_bound, "upper_bound": upper_bound,
            "original_count": len(group),
            "cleaned_count": mask.sum()
        }

        if visualize:
            import matplotlib.pyplot as plt
            import seaborn as sns

            plt.figure(figsize=(10,4))
            plt.subplot(1,2,1)
            sns.boxplot(y=prices)
            plt.title(f"Boxplot: {keys}")

            plt.subplot(1,2,2)
            sns.histplot(prices[mask], bins=20, kde=True)
            plt.title(f"Cleaned Distribution: {keys}")

            plt.tight_layout()
            plt.show()

    df_clean = df.loc[clean_indices].drop(columns=["_price_num"])
    return df_clean, stats_dict
