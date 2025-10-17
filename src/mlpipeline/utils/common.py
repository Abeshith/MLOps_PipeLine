import os
import yaml
import json
import joblib
from pathlib import Path
from typing import Any
from mlpipeline import logger

def read_yaml(path_to_yaml: Path) -> dict:
    """Read yaml file and returns content as dict"""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        logger.exception(e)
        raise e

def create_directories(path_to_directories: list, verbose=True):
    """Create list of directories"""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

def save_json(path: Path, data: dict):
    """Save json data"""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def download_file(url: str, filepath: str, chunk_size=1024):
    """Download file from url to filepath"""
    import requests
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        logger.info(f"Downloaded file from {url} to {filepath}")
        return filepath
    except Exception as e:
        logger.exception(f"Error downloading file from {url}: {str(e)}")
        raise e
    logger.info(f"json file saved at: {path}")

def load_bin(path: Path) -> Any:
    """Load binary data"""
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

def save_bin(data: Any, path: Path):
    """Save binary file"""
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")

def get_size(path: Path) -> str:
    """Get size in KB"""
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"
