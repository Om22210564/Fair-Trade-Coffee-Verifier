# Fair Trade Coffee Verifier

An offline, hackathon-ready AI agent that verifies whether a coffee product's claimed origin farm exists in a certified Fair Trade farm registry.

The app simulates a barcode lookup API using bundled mock JSON data, extracts `origin_farm_name`, checks it against a local CSV registry, and returns a verification verdict with certification details, trust score, and an AI-generated explanation.

## Features

- Offline barcode lookup using `data/mock_products.json`
- Certified farm verification using `data/certified_fair_trade_farms.csv`
- Exact farm-name registry matching
- Verified / Possible Greenwashing status
- Product and farm detail panels
- Certification information
- Deterministic trust score
- AI-style explanation generated locally with no network calls
- Modular Python architecture
- Streamlit UI with sidebar barcode entry
- File-based logging in `logs/app.log`
- Pytest coverage for the core verification cases

## Demo Barcodes

| Barcode | Expected result | Origin farm |
| --- | --- | --- |
| `001234567890` | Verified | Finca El Paraiso |
| `009876543210` | Possible Greenwashing | Mass Harvest Plantations Ltd. |

## Project Structure

```text
fair_trade_coffee_verifier/
  app.py
  data/
    certified_fair_trade_farms.csv
    mock_products.json
  logs/
  src/
    agent.py
    config.py
    logging_config.py
    models.py
    product_lookup.py
    registry.py
    verifier.py
  tests/
    test_verifier.py
  requirements.txt
  README.md
```

## Run Locally

```bash
cd fair_trade_coffee_verifier
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app is self-contained after dependencies are installed. It does not call Open Food Facts or any external AI service at runtime.

## Run Tests

```bash
cd fair_trade_coffee_verifier
python -m pytest
```

## How It Works

1. The user enters or scans a barcode.
2. `MockBarcodeLookup` loads the matching mock JSON payload.
3. The agent extracts `origin_farm_name`.
4. `FairTradeRegistry` loads the certified farms CSV.
5. `CoffeeVerifier` performs an exact normalized farm-name match.
6. The app displays product details, farm details, verification status, certification information, trust score, and a local AI-generated explanation.

## Notes

- The trust score is intentionally deterministic for demo clarity.
- A product is treated as verified only when the farm exists in the registry and has active certification status.
- A product is flagged as possible greenwashing when it uses sustainability claims but the claimed farm is not found in the registry.
