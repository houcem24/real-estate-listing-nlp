# Real-Estate Listing Amenity Extraction

Recovering missing amenity information from French real-estate listings by reading their free-text
descriptions.

In the scraped dataset (33,691 listings, 26 fields), most structured fields are empty: over 560,000 values
are missing. The free-text description, however, is always filled in and often mentions what the structured
fields leave out ("climatisation dans toutes les pièces", "place de parking"). This project fills the
air-conditioning, parking and bathroom fields from the descriptions so the data can feed a price model.

## How it works

1. Split each description into sentences.
2. Look for amenity keywords as whole words:

   | Field | Keywords |
   |---|---|
   | `climatisation` | climatisation, climatiseur, ventilation |
   | `fonds` (parking) | parking |
   | `salle_de_bain` | bain |

3. Copy the matching sentence into the empty field, keeping the original wording as evidence.

The exploration notebook profiles the missing values and also experiments with spaCy's French model
(`fr_core_news_md`): part-of-speech filtering and TextRank keyword extraction on the descriptions.

## Usage

```bash
git clone https://github.com/houcem24/real-estate-listing-nlp.git
cd real-estate-listing-nlp
pip install pandas
python extract_amenities.py listings.csv -o listings_enriched.csv
```

The script prints how many rows of each field were filled before and after. The input CSV needs a `description` column plus the three amenity
columns. Pass `--overwrite` to replace existing values as well as empty ones.

For the notebook:

```bash
pip install -r requirements.txt
python -m spacy download fr_core_news_md
jupyter notebook amenity_extraction_exploration.ipynb
```

The scraped listing data is not included in this repository.

## Repository structure

```
├── extract_amenities.py                  # Command-line tool
├── amenity_extraction_exploration.ipynb  # Exploration with spaCy and TextRank (comments in French)
└── requirements.txt
```

## Limitations and next steps

- Keyword matching misses synonyms and negations ("pas de parking" is counted as a parking mention).
- A next step would be a small classifier or spaCy `Matcher` patterns that also return a yes/no value, so the
  filled fields can go straight into a price-prediction model.

## Context

NLP project at ESPRIT (2023).

## License

[MIT](LICENSE)
