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
    # Normalize to 2-char field (strip then right)
    s = (s or "").strip().upper()[:2]
    return s.ljust(2)


def load_data(csv_path: str | Path = None):
    """Clear and load voter records from CSV into the database."""
    Voter.objects.all().delete()

    if csv_path is None:
        # Put CSV at voter_analytics/data/newton_voters.csv
        csv_path = Path(__file__).resolve().parent / "data" / "newton_voters.csv"
    csv_path = Path(csv_path)

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader, None)  # Skip header row

        for row in reader:
            # Cateogory orders:
            try:
                voter = Voter(
                    last_name=row[0].strip(),
                    first_name=row[1].strip(),
                    street_number=row[2].strip(),
                    street_name=row[3].strip(),
                    apartment_number=row[4].strip() or None,
                    zip_code=row[5].strip(),
                    date_of_birth=_parse_date(row[6]),
                    date_of_registration=_parse_date(row[7]),
                    party_affiliation=_party_two_chars(row[8]),
                    precinct_number=row[9].strip(),
                    v20state=_parse_bool(row[10]),
                    v21town=_parse_bool(row[11]),
                    v21primary=_parse_bool(row[12]),
                    v22general=_parse_bool(row[13]),
                    v23town=_parse_bool(row[14]),
                    voter_score=int((row[15] or "0").strip() or 0),
                )
                voter.save()
            except Exception as e:
                print("Skipped row due to error:", e, "Row:", row)

    print(f"Loaded {Voter.objects.count()} voters.")
