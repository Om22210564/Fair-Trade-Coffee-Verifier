from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    barcode: str
    product_name: str
    brand: str
    labels: str
    manufacturing_places: str
    origin_farm_name: str


@dataclass(frozen=True)
class Farm:
    registry_id: str
    farm_name: str
    country: str
    certification_year: str
    status: str


@dataclass(frozen=True)
class VerificationResult:
    product: Product
    matched_farm: Optional[Farm]
    status: str
    trust_score: int
    certification_information: str
    explanation: str
