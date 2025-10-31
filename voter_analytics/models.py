# File: voter_analytics/models.py
# Author: Louise Lee, llouise@bu.edu, 10/28/2025
# Description: Models define the fields (columns) of database, specifying data types, values, rules

from django.db import models
from pathlib import Path
from datetime import datetime
import csv


class Voter(models.Model):
    """Encapsulate data of individual profile"""

    # Identification
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)

    # Address
    street_number = models.TextField(blank=True, null=True)
    street_name = models.TextField(blank=True, null=True)
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.TextField(blank=True, null=True)

    # Voter information
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=2, blank=True, null=True)
    precinct_number = models.TextField(blank=True, null=True)

    # Election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    # Admin comment
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.street_number} {self.street_name}, Precinct {self.precinct_number}"


def _parse_date(s: str):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def _parse_bool(s: str):
    return (s or "").strip().upper() in {"TRUE", "T", "YES", "Y", "1"}


def _party_two_chars(s: str) -> str:
    # Normalize to 2-char field (strip then pad to 2 chars)
    s = (s or "").strip().upper()[:2]
    return s.ljust(2)


def load_data(csv_path: str | Path = None):
    """Clear and load voter records from CSV into the database."""
    Voter.objects.all().delete()

    if csv_path is None:
        # Put CSV at voter_analytics/data/newton_voters.csv
        csv_path = Path(__file__).resolve().parent / "data" / "newton_voters.csv"
    csv_path = Path(csv_path)

    loaded_count = 0
    skipped_count = 0

    with csv_path.open(newline="", encoding="utf-8") as f:
        # Use DictReader to handle headers automatically
        reader = csv.DictReader(f)

        # Debug: Print field names
        print(f"CSV Fields: {reader.fieldnames}")

        # Clean up field names (strip spaces)
        reader.fieldnames = [
            field.strip() if field else field for field in reader.fieldnames
        ]
        print(f"Cleaned Fields: {reader.fieldnames}")

        for line_num, row in enumerate(reader, start=2):
            try:
                # Access by column name instead of index
                # Note: Voter ID Number is in the CSV but we don't store it
                voter = Voter(
                    last_name=(row.get("Last Name") or "").strip(),
                    first_name=(row.get("First Name") or "").strip(),
                    street_number=(
                        row.get("Residential Address - Street Number") or ""
                    ).strip(),
                    street_name=(
                        row.get("Residential Address - Street Name") or ""
                    ).strip(),
                    apartment_number=(
                        row.get("Residential Address - Apartment Number") or ""
                    ).strip()
                    or None,
                    zip_code=(row.get("Residential Address - Zip Code") or "").strip(),
                    date_of_birth=_parse_date(row.get("Date of Birth") or ""),
                    date_of_registration=_parse_date(
                        row.get("Date of Registration") or ""
                    ),
                    party_affiliation=_party_two_chars(
                        row.get("Party Affiliation") or ""
                    ),
                    precinct_number=(row.get("Precinct Number") or "").strip(),
                    v20state=_parse_bool(row.get("v20state") or ""),
                    v21town=_parse_bool(row.get("v21town") or ""),
                    v21primary=_parse_bool(row.get("v21primary") or ""),
                    v22general=_parse_bool(row.get("v22general") or ""),
                    v23town=_parse_bool(row.get("v23town") or ""),
                    voter_score=int(((row.get("voter_score") or "0").strip() or "0")),
                )
                voter.save()
                loaded_count += 1

            except Exception as e:
                print("Skipped row due to error:", e, "Row:", row)

    print(f"Loaded {Voter.objects.count()} voters.")
