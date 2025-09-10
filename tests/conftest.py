# Test configuration and fixtures
import pytest
import os
import sys
import tempfile
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session")
def sample_data():
    """Create sample data for testing"""
    np.random.seed(42)
    data = {
        'age': np.random.randint(18, 80, 100),
        'job': np.random.choice(['admin', 'technician', 'management'], 100),
        'marital': np.random.choice(['married', 'single', 'divorced'], 100),
        'education': np.random.choice(['primary', 'secondary', 'tertiary'], 100),
        'default': np.random.choice(['no', 'yes'], 100),
        'balance': np.random.randint(0, 10000, 100),
        'housing': np.random.choice(['no', 'yes'], 100),
        'loan': np.random.choice(['no', 'yes'], 100),
        'contact': np.random.choice(['cellular', 'telephone'], 100),
        'duration': np.random.randint(0, 1000, 100),
        'campaign': np.random.randint(1, 10, 100),
        'pdays': np.random.randint(-1, 999, 100),
        'previous': np.random.randint(0, 10, 100),
        'poutcome': np.random.choice(['success', 'failure', 'other'], 100),
        'y': np.random.choice(['no', 'yes'], 100)
    }
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def temp_artifacts_dir():
    """Create temporary artifacts directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        artifacts_dir = os.path.join(temp_dir, 'artifacts')
        os.makedirs(artifacts_dir, exist_ok=True)
        yield artifacts_dir

@pytest.fixture(scope="session")
def test_config():
    """Test configuration"""
    return {
        'test_data_size': 100,
        'random_seed': 42,
        'expected_columns': [
            'age', 'job', 'marital', 'education', 'default',
            'balance', 'housing', 'loan', 'contact', 'duration',
            'campaign', 'pdays', 'previous', 'poutcome', 'y'
        ]
    }

@pytest.fixture
def mock_model_path(temp_artifacts_dir):
    """Mock model file path"""
    model_dir = os.path.join(temp_artifacts_dir, 'model_trainer')
    os.makedirs(model_dir, exist_ok=True)
    return os.path.join(model_dir, 'model.pkl')

@pytest.fixture
def mock_preprocessor_path(temp_artifacts_dir):
    """Mock preprocessor file path"""
    preprocessor_dir = os.path.join(temp_artifacts_dir, 'data_transformation')
    os.makedirs(preprocessor_dir, exist_ok=True)
    return os.path.join(preprocessor_dir, 'preprocessor.pkl')
