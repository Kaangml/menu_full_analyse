import pandas as pd
import re
import unicodedata

from config import INPUT_PATH, OUTPUT_PATH, SHEET_NAME
from rules import (
    wine_rules, vodka_rules, gin_rules, raki_rules,
    liqueur_rules, rum_rules, tequila_rules, mezcal_rules,
    cocktail_rules, vermut_rules, whisky_rules,cognac_rules, shot_rules
)
from rules import beer_rules as br
from rules.common import normalize, extract_volume, normalize_brand,clean_price_iqr_grouped

# ---------------------------
# CATEGORY DETECTION
# ---------------------------
def detect_category(row):
    name, cat = str(row.get("Product Name","")), str(row.get("Category",""))

    # 1) Bira
    if br.detect_beer(name, cat):
        return "Bira"
    # 2) Şarap
    if wine_rules.detect_wine(name, cat):
        return "Şarap"
    # 3) Vodka
    if vodka_rules.detect_vodka(name, cat):
        return "Vodka"
    # 4) Gin
    if gin_rules.detect_gin(name, cat):
        return "Cin"
    # 5) Rakı
    if raki_rules.detect_raki(name, cat):
        return "Rakı"
    # 6) Likör
    if liqueur_rules.detect_liqueur(name, cat):
        return "Likör"
    # 7) Rom
    if rum_rules.detect_rum(name, cat):
        return "Rom"
    # 8) Tekila
    if tequila_rules.detect_tequila(name,cat):
        return "Tekila"
    # 9) Mezcal
    if mezcal_rules.detect_mezcal(name,cat):
        return "Mezcal"
    # 10) Vermut
    if vermut_rules.detect_vermut(name):
        return "Vermut"
    # 11) Kokteyl
    if cocktail_rules.detect_cocktail(name,cat):
        return "Kokteyl"
    if whisky_rules.detect_whisky(name, cat):
        return "Viski"
    if cognac_rules.detect_cognac(name, cat):
        return "Konyak"
    if shot_rules.detect_shot(name, cat):
        return "Shot"

    return "Diğer"

def detect_subcategory(row):
    cat = row["Ana Kategori"]
    name, cat_field = str(row.get("Product Name","")), str(row.get("Category",""))

    if cat == "Bira":
        return br.detect_beer_sub(name, cat_field)
    if cat == "Şarap":
        return wine_rules.detect_wine_sub(name, cat_field)
    if cat == "Vodka":
        return vodka_rules.detect_vodka(name)
    if cat == "Cin":
        return gin_rules.detect_gin_sub(name,cat_field)
    if cat == "Rakı":
        return raki_rules.detect_raki_sub(name,cat_field)
    if cat == "Likör":
        return liqueur_rules.detect_liqueur(name)
    if cat == "Rom":
        return rum_rules.detect_rum(name)
    if cat == "Tekila":
        return tequila_rules.detect_tequila(name)
    if cat == "Mezcal":
        return mezcal_rules.detect_mezcal(name)
    if cat == "Vermut":
        return vermut_rules.detect_vermut(name)
    if cat == "Kokteyl":
        return cocktail_rules.detect_cocktail_sub(name, cat_field)
    if cat == "Viski":
        return whisky_rules.detect_whisky_sub(name, cat_field)
    if cat == "Konyak":
        return cognac_rules.detect_cognac_sub(name, cat_field)


    return None

# ---------------------------
# MAIN PROCESS
# ---------------------------
def process_dataframe(df):
    df = df.copy()
    df["Mapin ID"] = df["Mapin ID"]
    df["Product Name"] = df["Product Name"]
    df["pn_l"]  = df["Product Name"].apply(normalize) if "Product Name" in df.columns else ""
    df["cat_l"] = df["Category"].apply(normalize)      if "Category" in df.columns else ""
    df["ic_l"]  = df["İçerik"].apply(normalize)        if "İçerik" in df.columns else ""

    df["Ana Kategori"] = df.apply(detect_category, axis=1)
    df["Alt Kategori"] = df.apply(detect_subcategory, axis=1)
    df["Hacim"] = df.apply(lambda x: extract_volume(x["Product Name"], x.get("CL")), axis=1)
    df["Marka"] = df["Product Name"].apply(normalize_brand)
    # Sadece Ana Kategori 'Bira' olan satırlar için
    is_beer = df["Ana Kategori"] == "Bira"
    # Ambalaj Tipi
    df.loc[is_beer, "Ambalaj Tipi"] = df.loc[is_beer].apply(
        lambda x: br.extract_package(x["Product Name"], x.get("Category","")), axis=1
    )

    # Bira Stili
    df["Kat_Style"] = df.apply(br.detect_style, axis=1)

    # Segment
    df.loc[is_beer, "Segment"] = df.loc[is_beer, "Product Name"].apply(br.detect_beer_segment)

    return df

def main():
    df_all = pd.read_excel(INPUT_PATH, sheet_name=SHEET_NAME)
    df_proc = process_dataframe(df_all)
    #df_proc.to_excel(OUTPUT_PATH, index=False)
    print(f"✅ Tüm kategoriler işlendi -> {OUTPUT_PATH}")


        # ---------- Özet & Kaydet ----------
    ana_counts   = df_proc["Ana Kategori"].value_counts().reset_index()
    ana_counts.columns = ["Ana Kategori", "Adet"]

    alt_counts   = df_proc["Alt Kategori"].value_counts().reset_index()
    alt_counts.columns = ["Alt Kategori", "Adet"]

    style_counts = df_proc["Kat_Style"].value_counts().reset_index()
    style_counts.columns = ["Kat_Style", "Adet"]

    segment_counts = df_proc["Segment"].value_counts().reset_index()
    segment_counts.columns = ["Segment", "Adet"]


    df_clean, stats = clean_price_iqr_grouped(
        df_proc,
        price_col="Price",
        group_cols=["Ana Kategori", "Hacim"],
        visualize=True
    )

    with pd.ExcelWriter(OUTPUT_PATH, engine="xlsxwriter") as writer:
        df_proc.to_excel(writer, index=False, sheet_name="Veri")
        ana_counts.to_excel(writer, index=False, sheet_name="Ana_Kategori_Dagilimi")
        alt_counts.to_excel(writer, index=False, sheet_name="Alt_Kategori_Dagilimi")
        style_counts.to_excel(writer, index=False, sheet_name="Stil_Dagilimi")
        segment_counts.to_excel(writer, index=False, sheet_name="Segment_Dagilimi")
        df_clean.to_excel(writer, index=False, sheet_name="Fiyat_Temizlendi")



if __name__ == "__main__":
    main()
