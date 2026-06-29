from .models import Farm, Product, VerificationResult
from .registry import FairTradeRegistry


VERIFIED = "Verified"
POSSIBLE_GREENWASHING = "Possible Greenwashing"


class CoffeeVerifier:
    def __init__(self, registry: FairTradeRegistry) -> None:
        self.registry = registry

    def verify(self, product: Product) -> VerificationResult:
        farm = self.registry.find_exact(product.origin_farm_name)
        is_verified = farm is not None and farm.status.casefold() == "active"

        status = VERIFIED if is_verified else POSSIBLE_GREENWASHING
        trust_score = self._calculate_trust_score(product, farm, is_verified)
        certification_information = self._certification_information(farm)
        explanation = self._generate_explanation(product, farm, status, trust_score)

        return VerificationResult(
            product=product,
            matched_farm=farm,
            status=status,
            trust_score=trust_score,
            certification_information=certification_information,
            explanation=explanation,
        )

    @staticmethod
    def _calculate_trust_score(product: Product, farm: Farm | None, is_verified: bool) -> int:
        if not is_verified:
            score = 28
            label_text = product.labels.casefold()
            if any(term in label_text for term in ("fair trade", "sustainable", "eco-friendly")):
                score -= 8
            return max(score, 10)

        score = 82
        if "fair trade" in product.labels.casefold():
            score += 10
        if farm and farm.status.casefold() == "active":
            score += 8
        return min(score, 100)

    @staticmethod
    def _certification_information(farm: Farm | None) -> str:
        if farm is None:
            return (
                "No matching farm certification was found in the offline Fair Trade registry."
            )

        return (
            f"{farm.farm_name} is listed as {farm.status} under registry "
            f"{farm.registry_id}, certified in {farm.certification_year} in {farm.country}."
        )

    @staticmethod
    def _generate_explanation(
        product: Product, farm: Farm | None, status: str, trust_score: int
    ) -> str:
        if farm:
            return (
                f"The product claims origin from {product.origin_farm_name}. That farm is an "
                f"exact match in the certified registry with {farm.status.lower()} status, so "
                f"the sourcing claim is treated as {status.lower()}. The trust score is "
                f"{trust_score}/100 because both the product origin and registry record align."
            )

        return (
            f"The product claims origin from {product.origin_farm_name}, but that farm name does "
            f"not appear in the certified registry. Because the label uses ethical or sustainability "
            f"language without a registry match, the agent flags this as {status.lower()} with a "
            f"trust score of {trust_score}/100."
        )
