from .logging_config import configure_logging
from .models import VerificationResult
from .product_lookup import MockBarcodeLookup
from .registry import FairTradeRegistry
from .verifier import CoffeeVerifier


class FairTradeCoffeeAgent:
    def __init__(
        self,
        lookup: MockBarcodeLookup | None = None,
        registry: FairTradeRegistry | None = None,
    ) -> None:
        self.logger = configure_logging()
        self.lookup = lookup or MockBarcodeLookup()
        self.registry = registry or FairTradeRegistry()
        self.verifier = CoffeeVerifier(self.registry)

    def verify_barcode(self, barcode: str) -> VerificationResult:
        self.logger.info("Starting verification for barcode=%s", barcode)
        product = self.lookup.lookup(barcode)
        result = self.verifier.verify(product)
        self.logger.info(
            "Verification complete barcode=%s farm=%s status=%s score=%s",
            product.barcode,
            product.origin_farm_name,
            result.status,
            result.trust_score,
        )
        return result

    def sample_barcodes(self) -> list[str]:
        return self.lookup.available_barcodes()
