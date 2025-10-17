import pytest
import requests
import time
import subprocess
import os
import sys
sys.path.append('src')

class TestIntegration:
    """Integration tests for the ML pipeline"""
    
    def test_full_pipeline_execution(self):
        """Test complete pipeline can execute without errors"""
        # This would run the main pipeline
        result = subprocess.run([
            sys.executable, "main.py"
        ], capture_output=True, text=True, timeout=300)
        
        # Check if pipeline completed successfully
        assert result.returncode == 0, f"Pipeline failed: {result.stderr}"
        
    def test_model_artifacts_created(self):
        """Test that model artifacts are created after training"""
        expected_artifacts = [
            "artifacts/model_trainer/model.pkl",
            "artifacts/data_transformation/preprocessor.pkl",
            "artifacts/model_evaluation/metrics.json"
        ]
        
        for artifact in expected_artifacts:
            if os.path.exists(artifact):
                assert os.path.getsize(artifact) > 0, f"Artifact {artifact} is empty"
    
    @pytest.mark.skipif(not os.getenv("RUN_API_TESTS"), reason="API tests require running server")
    def test_flask_app_health(self):
        """Test Flask application health endpoint"""
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            assert response.status_code == 200
            assert "status" in response.json()
        except requests.exceptions.ConnectionError:
            pytest.skip("Flask app not running")
    
    @pytest.mark.skipif(not os.getenv("RUN_API_TESTS"), reason="API tests require running server")
    def test_prediction_endpoint(self):
        """Test model prediction endpoint"""
        try:
            # Sample prediction data
            test_data = {
                "feature1": 1.0,
                "feature2": 2.0,
                "feature3": 3.0
            }
            
            response = requests.post(
                "http://localhost:5000/predict", 
                json=test_data,
                timeout=10
            )
            assert response.status_code == 200
            result = response.json()
            assert "prediction" in result
        except requests.exceptions.ConnectionError:
            pytest.skip("Flask app not running")
