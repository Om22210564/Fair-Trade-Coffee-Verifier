import json
from pathlib import Path
from typing import Any

from .config import MOCK_PRODUCTS_PATH
from .models import Product


class ProductLookupError(Exception):
    """Raised when a barcode cannot be resolved to a usable product."""


class MockBarcodeLookup:
    def __init__(self, data_path: Path = MOCK_PRODUCTS_PATH) -> None:
        self.data_path = data_path
        self._products = self._load_products()

    def available_barcodes(self) -> list[str]:
        return sorted(self._products.keys())

    def lookup(self, barcode: str) -> Product:
        normalized = self._normalize_barcode(barcode)
        payload = self._products.get(normalized)

        if payload is None:
            raise ProductLookupError(
                f"Barcode {normalized or barcode!r} was not found in the offline mock lookup source."
            )

        if payload.get("status") != 1 or not isinstance(payload.get("product"), dict):
            raise ProductLookupError(f"Barcode {normalized!r} returned an invalid product payload.")

        product = payload["product"]
        origin_farm_name = str(product.get("origin_farm_name", "")).strip()
        if not origin_farm_name:
            raise ProductLookupError(
                f"Barcode {normalized!r} does not include origin_farm_name."
            )

        return Product(
            barcode=normalized,
            product_name=str(product.get("product_name", "Unknown product")).strip(),
            brand=str(product.get("brands", "Unknown brand")).strip(),
            labels=str(product.get("labels", "No labels provided")).strip(),
            manufacturing_places=str(
                product.get("manufacturing_places", "Unknown manufacturing place")
            ).strip(),
            origin_farm_name=origin_farm_name,
        )

    def _load_products(self) -> dict[str, dict[str, Any]]:
        try:
            with self.data_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise ProductLookupError(f"Mock product data file is missing: {self.data_path}") from exc
        except json.JSONDecodeError as exc:
            raise ProductLookupError(f"Mock product data file is not valid JSON: {exc}") from exc

        if not isinstance(data, dict):
            raise ProductLookupError("Mock product data must be a JSON object keyed by barcode.")

        return data

    @staticmethod
    def _normalize_barcode(barcode: str) -> str:
        return "".join(character for character in barcode.strip() if character.isdigit())
