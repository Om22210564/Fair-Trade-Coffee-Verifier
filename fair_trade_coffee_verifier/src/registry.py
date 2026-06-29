import csv
from pathlib import Path

from .config import CERTIFIED_FARMS_PATH
from .models import Farm


class RegistryError(Exception):
    """Raised when the certified farm registry cannot be loaded."""


class FairTradeRegistry:
    def __init__(self, csv_path: Path = CERTIFIED_FARMS_PATH) -> None:
        self.csv_path = csv_path
        self._farms = self._load_farms()
        self._farm_index = {self._normalize(farm.farm_name): farm for farm in self._farms}

    def find_exact(self, farm_name: str) -> Farm | None:
        return self._farm_index.get(self._normalize(farm_name))

    def all_farms(self) -> list[Farm]:
        return list(self._farms)

    def _load_farms(self) -> list[Farm]:
        try:
            with self.csv_path.open("r", encoding="utf-8-sig", newline="") as file:
                rows = list(csv.DictReader(file))
        except FileNotFoundError as exc:
            raise RegistryError(f"Certified farm registry is missing: {self.csv_path}") from exc

        required_columns = {
            "Registry_ID",
            "Farm_Name",
            "Country",
            "Certification_Year",
            "Status",
        }
        if not rows:
            raise RegistryError("Certified farm registry is empty.")
        if not required_columns.issubset(rows[0].keys()):
            missing = ", ".join(sorted(required_columns - set(rows[0].keys())))
            raise RegistryError(f"Certified farm registry is missing columns: {missing}")

        farms = [
            Farm(
                registry_id=row["Registry_ID"].strip(),
                farm_name=row["Farm_Name"].strip(),
                country=row["Country"].strip(),
                certification_year=row["Certification_Year"].strip(),
                status=row["Status"].strip(),
            )
            for row in rows
        ]
        return farms

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(value.casefold().strip().split())
