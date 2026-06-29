from src.agent import FairTradeCoffeeAgent
from src.verifier import POSSIBLE_GREENWASHING, VERIFIED


def test_verified_barcode_has_high_trust_score():
    agent = FairTradeCoffeeAgent()

    result = agent.verify_barcode("001234567890")

    assert result.status == VERIFIED
    assert result.matched_farm is not None
    assert result.matched_farm.registry_id == "FT-8819"
    assert result.trust_score == 100


def test_unregistered_farm_is_flagged():
    agent = FairTradeCoffeeAgent()

    result = agent.verify_barcode("009876543210")

    assert result.status == POSSIBLE_GREENWASHING
    assert result.matched_farm is None
    assert result.trust_score == 20
