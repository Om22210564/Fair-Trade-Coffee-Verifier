from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

MOCK_PRODUCTS_PATH = DATA_DIR / "mock_products.json"
CERTIFIED_FARMS_PATH = DATA_DIR / "certified_fair_trade_farms.csv"
LOG_FILE_PATH = LOG_DIR / "app.log"
