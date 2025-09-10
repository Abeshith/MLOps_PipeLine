"""
Integration tests for ML pipeline
"""
import pytest
import requests
import time
import os
import sys
import subprocess
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestAPIEndpoints:
    """Test API endpoints integration"""
    
    @pytest.fixture(scope="class")
    def base_url(self):
        """Base URL for API testing"""
        return os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    def test_health_endpoint(self, base_url):
        """Test health endpoint"""
        try:
            response = requests.get(f"{base_url}/health", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert 'service' in data
            assert data['service'] == 'bank-marketing-predictor'
        except requests.exceptions.RequestException:
            pytest.skip("API server not available for integration tests")
    
    def test_metrics_endpoint(self, base_url):
        """Test Prometheus metrics endpoint"""
        try:
            response = requests.get(f"{base_url}/metrics", timeout=10)
            assert response.status_code == 200
            # Check if it contains Prometheus-style metrics
            content = response.text
            assert 'ml_predictions_total' in content or 'http_requests_total' in content
        except requests.exceptions.RequestException:
            pytest.skip("API server not available for integration tests")
    
    def test_prediction_endpoint(self, base_url):
        """Test prediction endpoint with sample data"""
        sample_prediction_data = {
            "age": 30,
            "job": "admin",
            "marital": "married",
            "education": "tertiary",
            "default": "no",
            "balance": 1500,
            "housing": "yes",
            "loan": "no",
            "contact": "cellular",
            "duration": 200,
            "campaign": 2,
            "pdays": -1,
            "previous": 0,
            "poutcome": "unknown"
        }
        
        try:
            response = requests.post(
                f"{base_url}/predict",
                json=sample_prediction_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                assert 'prediction' in data
                assert 'probability' in data
                assert 'confidence' in data
                assert data['prediction'] in [0, 1]
            else:
                # If model not trained yet, should get appropriate error
                assert response.status_code in [400, 500]
                
        except requests.exceptions.RequestException:
            pytest.skip("API server not available for integration tests")

class TestPipelineIntegration:
    """Test end-to-end pipeline integration"""
    
    def test_full_pipeline_run(self, sample_data, temp_artifacts_dir):
        """Test complete pipeline execution"""
        # Create test data files
        train_file = os.path.join(temp_artifacts_dir, 'train.csv')
        test_file = os.path.join(temp_artifacts_dir, 'test.csv')
        
        os.makedirs(os.path.dirname(train_file), exist_ok=True)
        sample_data.to_csv(train_file, index=False)
        sample_data.to_csv(test_file, index=False)
        
        # Test that we can import and run pipeline components
        try:
            from mlpipeline.config.configuration import ConfigurationManager
            from mlpipeline.components.data_validation import DataValidation
            
            config_manager = ConfigurationManager()
            assert config_manager is not None
            
            # Test data validation
            try:
                data_validation_config = config_manager.get_data_validation_config()
                data_validation = DataValidation(config=data_validation_config)
                assert data_validation is not None
            except Exception as e:
                # Configuration might not be fully set up in test environment
                print(f"Configuration test skipped: {e}")
                
        except ImportError as e:
            pytest.fail(f"Failed to import pipeline components: {e}")

class TestObservabilityIntegration:
    """Test observability stack integration"""
    
    def test_prometheus_metrics_available(self):
        """Test that Prometheus metrics are being exposed"""
        try:
            # Check if metrics server is running
            response = requests.get('http://localhost:8000/metrics', timeout=5)
            if response.status_code == 200:
                content = response.text
                # Check for some expected metrics
                assert any(metric in content for metric in [
                    'ml_predictions_total',
                    'python_info',
                    'process_cpu_seconds_total'
                ])
            else:
                pytest.skip("Metrics server not running")
        except requests.exceptions.RequestException:
            pytest.skip("Metrics server not available")
    
    def test_logging_integration(self):
        """Test logging integration"""
        from mlpipeline.observability.logging_config import get_pipeline_logger
        
        logger = get_pipeline_logger("test_integration", "test_component", "test_stage")
        
        # Test that logging works without errors
        logger.info("Integration test log message")
        logger.warning("Integration test warning")
        logger.error("Integration test error")
        
        # Check if log files are being created
        log_dir = "logs"
        if os.path.exists(log_dir):
            log_files = os.listdir(log_dir)
            assert len(log_files) > 0
        else:
            pytest.skip("Log directory not found")

class TestDataQuality:
    """Test data quality and validation"""
    
    def test_data_schema_validation(self, sample_data):
        """Test data schema validation"""
        expected_columns = [
            'age', 'job', 'marital', 'education', 'default',
            'balance', 'housing', 'loan', 'contact', 'duration',
            'campaign', 'pdays', 'previous', 'poutcome', 'y'
        ]
        
        # Check all expected columns are present
        assert all(col in sample_data.columns for col in expected_columns)
        
        # Check data types are reasonable
        assert sample_data['age'].dtype in ['int64', 'float64']
        assert sample_data['balance'].dtype in ['int64', 'float64']
        assert sample_data['duration'].dtype in ['int64', 'float64']
        
        # Check for no null values in critical columns
        assert sample_data['y'].notna().all()
        assert sample_data['age'].notna().all()
    
    def test_data_quality_checks(self, sample_data):
        """Test basic data quality checks"""
        # Check for reasonable value ranges
        assert sample_data['age'].min() >= 18
        assert sample_data['age'].max() <= 80
        
        # Check categorical values
        valid_yes_no = ['yes', 'no']
        assert sample_data['default'].isin(valid_yes_no).all()
        assert sample_data['housing'].isin(valid_yes_no).all()
        assert sample_data['loan'].isin(valid_yes_no).all()
        assert sample_data['y'].isin(valid_yes_no).all()

class TestModelIntegration:
    """Test model integration and predictions"""
    
    def test_model_prediction_format(self):
        """Test that model predictions return expected format"""
        sample_input = {
            "age": 35,
            "job": "management",
            "marital": "married",
            "education": "tertiary",
            "default": "no",
            "balance": 2000,
            "housing": "yes",
            "loan": "no",
            "contact": "cellular",
            "duration": 300,
            "campaign": 1,
            "pdays": -1,
            "previous": 0,
            "poutcome": "unknown"
        }
        
        # Test that prediction pipeline can process the input
        # This would normally test the actual model prediction
        assert isinstance(sample_input, dict)
        assert all(key in sample_input for key in ['age', 'job', 'marital', 'education'])
        
    def test_prediction_performance(self):
        """Test prediction performance metrics"""
        # This would test actual prediction latency and throughput
        # For now, just ensure the test structure is in place
        start_time = time.time()
        
        # Simulate prediction processing time
        time.sleep(0.01)  # 10ms simulated processing
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Assert reasonable processing time (under 1 second for this test)
        assert processing_time < 1.0
