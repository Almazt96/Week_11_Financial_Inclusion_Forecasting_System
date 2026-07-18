"""
Core data loading and preprocessing module.
Handles ingestion, structural validation, and type casting with explicit error boundaries.
"""
import sys
import os

# Adds the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config  # Your original import will work fine now!
import logging
import pandas as pd
from typing import Optional
from src import config

# Set up logging for tracking pipeline execution
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_and_validate_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Loads a CSV file into a DataFrame, verifies the schema, and converts data types.

    Parameters:
    -----------
    file_path : str
        The absolute or relative path to the source CSV file.

    Returns:
    --------
    Optional[pd.DataFrame]
        A cleaned and typed DataFrame if successful; None if a critical error occurs.

    Raises:
    -------
    FileNotFoundError, KeyError, ValueError (Caught internally and logged)
    """
    # 1. Handle File Loading Errors
    try:
        logger.info(f"Attempting to load data from: {file_path}")
        df = pd.read_csv(file_path)
        logger.info("File loaded successfully.")
    except FileNotFoundError as e:
        logger.error(f"Critical Error: The file at {file_path} does not exist. Details: {e}")
        return None
    except pd.errors.EmptyDataError as e:
        logger.error(f"Critical Error: The file at {file_path} is empty. Details: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while reading the file: {e}")
        return None

    # 2. Handle Missing Columns (Schema Validation)
    try:
        missing_cols = [col for col in config.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise KeyError(f"The following required columns are missing: {missing_cols}")
    except KeyError as e:
        logger.error(f"Schema Validation Failed: {e}")
        return None

    # 3. Handle Type Conversion Failures
    try:
        logger.info("Beginning data type conversions...")
        for column, data_type in config.TYPE_MAPPINGS.items():
            if data_type == "datetime64[ns]":
                df[column] = pd.to_datetime(df[column], errors="raise")
            else:
                df[column] = df[column].astype(data_type)
        logger.info("Data type conversions completed successfully.")
    except ValueError as e:
        logger.error(f"Data Type Conversion Failed: Ensure data formats align with schema. Details: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during type casting: {e}")
        return None

    return df