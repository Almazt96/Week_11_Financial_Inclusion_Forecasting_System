"""
Configuration settings for the data pipeline.
Centralizes all paths, constants, and column requirements.
"""

from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw_data.csv"

# Data Schema & Expectations
REQUIRED_COLUMNS = ["date", "sales", "store_id", "feature_column"]

TYPE_MAPPINGS = {
    "date": "datetime64[ns]",
    "sales": "float64",
    "store_id": "int64"
}

# Forecasting / Modeling Constants
RANDOM_STATE = 42
TEST_SIZE = 0.2