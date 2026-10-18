"""Fill missing amenity fields in French real-estate listings from their free-text descriptions.

Most listings leave structured fields such as air conditioning, parking or bathroom empty, but mention them
in the description. This script splits each description into sentences and copies the sentence that mentions
an amenity into the matching column.

Example:
    python extract_amenities.py data/listings.csv -o data/listings_enriched.csv
"""

import argparse
import re

import pandas as pd

# Column to fill -> French keywords that signal the amenity in a description.
AMENITY_KEYWORDS = {
    "climatisation": {"climatisation", "climatiseur", "ventilation"},
    "fonds": {"parking"},
    "salle_de_bain": {"bain"},
}


def split_sentences(text: str) -> list[str]:
    """Split a description into sentences on '.' and '?'."""
    return [sentence.strip() for sentence in re.split(r"[.?]", text) if sentence.strip()]


def find_sentence(sentences: list[str], keywords: set[str]) -> str | None:
    """Return the last sentence containing one of the keywords as a whole word, or None."""
    match = None
    for sentence in sentences:
        if keywords & set(sentence.lower().split()):
            match = sentence
    return match


def fill_amenities(listings: pd.DataFrame, overwrite: bool = False) -> pd.DataFrame:
    """Fill amenity columns from the description column.

    By default only empty fields are filled; with overwrite=True every field that has a matching sentence
    is replaced.
    """
    result = listings[[*AMENITY_KEYWORDS, "description"]].copy()
    # Amenity columns hold text after filling; empty columns would otherwise load as floats.
    result[list(AMENITY_KEYWORDS)] = result[list(AMENITY_KEYWORDS)].astype(object)
    sentences = result["description"].astype(str).map(split_sentences)

    for column, keywords in AMENITY_KEYWORDS.items():
        found = sentences.map(lambda s, kw=keywords: find_sentence(s, kw))
        target = found.notna() if overwrite else found.notna() & result[column].isna()
        result.loc[target, column] = found[target]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", help="CSV file with the listings (needs a 'description' column)")
    parser.add_argument("-o", "--output", default="listings_enriched.csv", help="Where to write the result")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing values, not only empty ones")
    args = parser.parse_args()

    listings = pd.read_csv(args.input)
    enriched = fill_amenities(listings, overwrite=args.overwrite)

    for column in AMENITY_KEYWORDS:
        before = listings[column].notna().sum()
        after = enriched[column].notna().sum()
        print(f"{column:>15}: {before:>6} -> {after:>6} filled rows")

    enriched.to_csv(args.output, index=False)
    print(f"Saved {len(enriched)} listings to {args.output}")


if __name__ == "__main__":
    main()
