"""
Unit tests for ML pipeline components
"""
import pytest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestDataValidation:
    """Test data validation component"""
    
    def test_validate_columns_success(self, sample_data, test_config):
        """Test successful column validation"""
        from mlpipeline.components.data_validation import DataValidation
        from mlpipeline.entity.config_entity import DataValidationConfig
        
        config = DataValidationConfig(
            root_dir="test_artifacts",
            validation_status_file="status.txt",
            drift_report_file="drift.html",
            data_quality_report_file="quality.json",
            schema={"columns": test_config['expected_columns']},
            validation_split=0.2,
            train_file_path="train.csv",
            test_file_path="test.csv"
        )
        
        # Mock the data files
        with patch('pandas.read_csv', return_value=sample_data):
            with patch('os.path.exists', return_value=True):
                validator = DataValidation(config=config)
                result = validator.validate_all_columns()
                assert result is not None

    def test_missing_columns_detection(self, test_config):
        """Test detection of missing columns"""
        from mlpipeline.components.data_validation import DataValidation
        from mlpipeline.entity.config_entity import DataValidationConfig
        
        # Create data with missing columns
        incomplete_data = pd.DataFrame({
            'age': [25, 30, 35],
            'job': ['admin', 'tech', 'mgmt']
        })
        
        config = DataValidationConfig(
            root_dir="test_artifacts",
            validation_status_file="status.txt",
            drift_report_file="drift.html",
            data_quality_report_file="quality.json",
            schema={"columns": test_config['expected_columns']},
            validation_split=0.2,
            train_file_path="train.csv",
            test_file_path="test.csv"
        )
        
        with patch('pandas.read_csv', return_value=incomplete_data):
            with patch('os.path.exists', return_value=True):
                validator = DataValidation(config=config)
                # This should detect missing columns
                with pytest.raises(Exception):
                    validator.validate_all_columns()

class TestFeatureEngineering:
    """Test feature engineering component"""
    
    def test_feature_creation(self, sample_data):
        """Test feature engineering processes"""
        from mlpipeline.components.feature_engineering import FeatureEngineering
        from mlpipeline.entity.config_entity import FeatureEngineeringConfig
        
        config = FeatureEngineeringConfig(
            root_dir="test_artifacts",
            engineered_features_dir="features",
            feature_importance_dir="importance",
            correlation_analysis_dir="correlation",
            feature_selection_dir="selection",
            train_data_path="train.csv",
            test_data_path="test.csv",
            processed_train_path="train_processed.csv",
            processed_test_path="test_processed.csv",
            feature_importance_path="importance.csv",
            feature_importance_plot_path="importance.png",
            correlation_matrix_path="correlation.csv",
            correlation_plot_path="correlation.png",
            feature_selection_report="selection.json"
        )
        
        # Mock file operations
        with patch('pandas.read_csv', return_value=sample_data):
            with patch('pandas.DataFrame.to_csv'):
                with patch('os.makedirs'):
                    with patch('matplotlib.pyplot.savefig'):
                        feature_eng = FeatureEngineering(config=config)
                        # This should run without errors
                        assert feature_eng is not None

class TestModelTrainer:
    """Test model training component"""
    
    def test_model_training(self, sample_data):
        """Test model training process"""
        from mlpipeline.components.model_trainer import ModelTrainer
        from mlpipeline.entity.config_entity import ModelTrainerConfig
        
        config = ModelTrainerConfig(
            root_dir="test_artifacts",
            train_data_path="train.csv",
            test_data_path="test.csv",
            model_name="model.pkl",
            target_column="y",
            expected_accuracy=0.6,
            model_params={"n_estimators": 100}
        )
        
        # Prepare data
        X = sample_data.drop(['y'], axis=1)
        y = sample_data['y']
        
        with patch('pandas.read_csv', return_value=sample_data):
            with patch('joblib.dump'):
                with patch('os.makedirs'):
                    trainer = ModelTrainer(config=config)
                    # This should initialize without errors
                    assert trainer is not None

class TestApp:
    """Test Flask application"""
    
    def test_health_endpoint_with_model(self, mock_model_path):
        """Test health endpoint when model exists"""
        import sys
        import os
        
        # Add the main directory to path to import app
        main_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        if main_dir not in sys.path:
            sys.path.insert(0, main_dir)
        
        with patch('os.path.exists', return_value=True):
            from app import app
            client = app.test_client()
            response = client.get('/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'healthy'

    def test_health_endpoint_without_model(self):
        """Test health endpoint when model doesn't exist"""
        import sys
        import os
        
        # Add the main directory to path to import app
        main_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        if main_dir not in sys.path:
            sys.path.insert(0, main_dir)
        
        with patch('os.path.exists', return_value=False):
            from app import app
            client = app.test_client()
            response = client.get('/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'degraded'

class TestObservability:
    """Test observability components"""
    
    def test_logging_setup(self):
        """Test logging configuration"""
        from mlpipeline.observability.logging_config import setup_logging, get_pipeline_logger
        
        # Test logger setup
        logger = get_pipeline_logger("test", "test_component", "test_stage")
        assert logger is not None
        
        # Test logging a message
        logger.info("Test log message")
        
    def test_metrics_collection(self):
        """Test metrics collection"""
        with patch('prometheus_client.start_http_server'):
            from mlpipeline.observability.metrics import pipeline_metrics
            
            # Test metrics recording
            pipeline_metrics.record_prediction_metrics("test_model", 0.1, True)
            pipeline_metrics.record_data_ingestion_metrics(1000, 0.5, True)
            
            # Should not raise any exceptions
            assert True
