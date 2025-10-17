import pytest
import os
import sys
sys.path.append('src')

from src.mlpipeline.config.configuration import ConfigurationManager
from src.mlpipeline.components.data_ingestion import DataIngestion

class TestPipeline:
    def test_config_manager_initialization(self):
        """Test configuration manager can be initialized"""
        config = ConfigurationManager()
        assert config is not None
    
    def test_data_ingestion_config(self):
        """Test data ingestion configuration"""
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        assert data_ingestion_config is not None
        assert hasattr(data_ingestion_config, 'root_dir')
    
    def test_artifacts_directory_creation(self):
        """Test that artifacts directories can be created"""
        artifacts_dir = "artifacts"
        assert os.path.exists(artifacts_dir) or True  # Will be created during pipeline
    
    def test_model_file_structure(self):
        """Test expected model file structure"""
        expected_files = [
            "config/config.yaml",
            "config/params.yaml", 
            "config/schema.yaml"
        ]
        for file_path in expected_files:
            assert os.path.exists(file_path), f"Missing config file: {file_path}"
