# Menu Category Analysis Pipeline

This project is designed to analyze and categorize menu items from a dataset, specifically focusing on alcoholic beverages. The pipeline processes the data, detects the main and subcategories of products, and generates a cleaned and categorized output.

---

## Table of Contents
1. [Overview](#overview)
2. [Business Logic](#business-logic)
3. [Pipeline Architecture](#pipeline-architecture)
4. [Data Pipeline](#data-pipeline)
5. [Setup and Usage](#setup-and-usage)

---

## Overview

The project processes menu data to:
- Detect the main category of products (e.g., beer, wine, vodka, etc.).
- Identify subcategories (e.g., "Blended Whisky", "Craft Beer").
- Extract additional details such as volume, packaging type, and brand.
- Clean outliers in pricing data using the IQR method.

The output is a structured dataset with detailed categorization and insights.

---

## Business Logic

The business logic is implemented in the `rules` directory, where each file corresponds to a specific category of beverages. The logic includes:

1. **Category Detection**:
   - Functions like `detect_beer`, `detect_wine`, and `detect_vodka` determine if a product belongs to a specific category based on keywords in the product name or category field.

2. **Subcategory Detection**:
   - Functions like `detect_whisky_sub` and `detect_gin_sub` identify subcategories based on additional keywords or patterns.

3. **Normalization**:
   - The `normalize` function in `rules/common.py` standardizes text by removing special characters and converting it to lowercase.

4. **Outlier Removal**:
   - The `clean_price_iqr_grouped` function removes pricing outliers using the IQR method, grouped by category and volume.

---

## Pipeline Architecture

The pipeline is structured as follows:

1. **Input**:
   - The input data is read from an Excel file (`efes_list.xlsx`) specified in `config.py`.

2. **Processing**:
   - The `pipeline.py` script processes the data:
     - Normalizes text fields.
     - Detects main and subcategories using rules from the `rules` directory.
     - Extracts additional details like volume, brand, and packaging type.
     - Cleans pricing data.

3. **Output**:
   - The processed data is saved to an Excel file (`efes_list_full_analyzed_pipeline_v2.xlsx`) with multiple sheets:
     - Processed data.
     - Distribution of main categories.
     - Distribution of subcategories.
     - Distribution of beer styles.
     - Distribution of segments.
     - Cleaned pricing data.

---

## Data Pipeline

### 1. **Input Data**
The input data is an Excel file containing the following columns:
- `Mapin ID`: Unique identifier for each product.
- `Product Name`: Name of the product.
- `Category`: Category field for the product.
- `İçerik`: Additional content information.
- `Price`: Price of the product.

### 2. **Processing Steps**
- **Normalization**:
  - Text fields are normalized using the `normalize` function.
- **Category Detection**:
  - The `detect_category` function determines the main category of each product.
- **Subcategory Detection**:
  - The `detect_subcategory` function identifies subcategories based on the main category.
- **Volume Extraction**:
  - The `extract_volume` function extracts volume information (e.g., "50cl", "shot").
- **Outlier Removal**:
  - The `clean_price_iqr_grouped` function removes pricing outliers.

### 3. **Output Data**
The output data includes:
- `Ana Kategori`: Main category of the product.
- `Alt Kategori`: Subcategory of the product.
- `Hacim`: Volume of the product.
- `Marka`: Brand of the product.
- `Ambalaj Tipi`: Packaging type (for beer).
- `Kat_Style`: Beer style (for beer).
- `Segment`: Segment classification (for beer).

---

## Setup and Usage

### Prerequisites
- Python 3.8+
- Required Python libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `xlsxwriter`

### Installation
1. Clone the repository.
2. Install the required libraries:
   ```bash
   pip install pandas matplotlib seaborn xlsxwriter
   ```

### Configuration
Update the `config.py` file with the correct paths for the input and output files:
```python
INPUT_PATH = "efes_list.xlsx"
OUTPUT_PATH = "efes_list_full_analyzed_pipeline_v2.xlsx"
SHEET_NAME = "MenuDetay"
```

### Running the Pipeline
Run the `pipeline.py` script:
```bash
python pipeline.py
```

The processed data will be saved to the output file specified in `config.py`.

---

## Directory Structure

```
├── config.py                # Configuration file for input/output paths
├── pipeline.py              # Main pipeline script
├── rules/                   # Business logic for category detection
│   ├── beer_rules.py        # Rules for beer detection
│   ├── wine_rules.py        # Rules for wine detection
│   ├── ...                  # Rules for other categories
│   └── common.py            # Common helper functions
├── efes_list.xlsx           # Input data file (ignored in .gitignore)
├── efes_list_full_analyzed_pipeline_v2.xlsx  # Output data file
└── .gitignore               # Ignore unnecessary files
```

---

## Notes
- The pipeline is modular, allowing easy addition of new categories or rules.
- The `rules` directory contains category-specific logic, making it easy to maintain and extend.
- The output includes detailed insights into the data, such as category distributions and cleaned pricing data.

---

## License
This project is for internal use only and is not licensed for external distribution.