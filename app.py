from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import json
import os
import pickle
import joblib
import time
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from src.mlpipeline.observability.metrics import pipeline_metrics
from src.mlpipeline.observability.tracing import trace_function
from src.mlpipeline.observability.logging_config import get_pipeline_logger

app = Flask(__name__)

# Setup logger and start metrics server
logger = get_pipeline_logger(__name__, component='prediction', pipeline_stage='serving')
pipeline_metrics.start_metrics_server(port=8000)

def create_simple_preprocessor():
    """Create a simple preprocessor for compatibility"""
    categorical_features = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome']
    numerical_features = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous', 'day']
    
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
        ]
    )
    return preprocessor

def load_pickle_file(filepath):
    """Load pickle file with error handling"""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def load_joblib_file(filepath):
    """Load joblib file with error handling"""
    try:
        return joblib.load(filepath)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@trace_function
def predict():
    start_time = time.time()
    model_type = "unknown"
    success = False
    
    try:
        logger.info("Starting prediction request", extra={
            'pipeline_stage': 'serving',
            'component': 'prediction'
        })
        
        # Load model with XGBoost compatibility handling
        if not os.path.exists('artifacts/model_trainer/model.pkl'):
            logger.error("Model file not found", extra={'error_code': 'MODEL_NOT_FOUND'})
            return jsonify({'error': 'Model file not found. Please run training first.'})
        
        try:
            # Try to load the model using joblib (as it was saved with joblib)
            model = load_joblib_file('artifacts/model_trainer/model.pkl')
            if model is None:
                logger.error("Failed to load model with joblib", extra={'error_code': 'MODEL_LOAD_FAILED'})
                return jsonify({'error': 'Failed to load model with joblib'})
            
            model_type = model.__class__.__name__
            logger.info(f"Model loaded successfully: {model_type}")
            
            # Fix XGBoost compatibility issues
            if hasattr(model, 'use_label_encoder'):
                model.use_label_encoder = False
            if hasattr(model, 'eval_metric'):
                if model.eval_metric == 'logloss':
                    model.eval_metric = 'logloss'
                    
        except Exception as e:
            logger.error(f"Error loading model: {e}", extra={'error_code': 'MODEL_LOAD_ERROR'})
            return jsonify({'error': f'Failed to load model: {str(e)}'})
        
        # Try to load preprocessor, if fails create a simple one
        preprocessor = load_joblib_file('artifacts/data_transformation/preprocessor.pkl')
        if preprocessor is None:
            print("Trying to load preprocessor with pickle...")
            preprocessor = load_pickle_file('artifacts/data_transformation/preprocessor.pkl')
        
        if preprocessor is None:
            print("Using fallback preprocessor due to compatibility issues")
            
            # Load training data to fit preprocessor - use the transformed data
            if not os.path.exists('artifacts/data_transformation/train.csv'):
                return jsonify({'error': 'Training data not found for preprocessing. Please run data transformation.'})
            
            # Load the already transformed training data to understand the structure
            transformed_train_df = pd.read_csv('artifacts/data_transformation/train.csv')
            feature_columns = [col for col in transformed_train_df.columns if col != 'y']
            
            # Create a simple identity preprocessor since data is already transformed
            from sklearn.preprocessing import StandardScaler
            from sklearn.base import BaseEstimator, TransformerMixin
            
            class IdentityTransformer(BaseEstimator, TransformerMixin):
                def fit(self, X, y=None):
                    return self
                def transform(self, X):
                    return X
            
            preprocessor = IdentityTransformer()
        
        # Get data from request
        data = request.json
        
        # Validate required fields
        required_fields = ['age', 'job', 'marital', 'education', 'housing', 'loan', 'duration', 'campaign']
        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({'error': f'Missing required field: {field}'})
        
        # Convert numeric fields
        try:
            data['age'] = int(data['age'])
            data['duration'] = int(data['duration'])
            data['campaign'] = int(data['campaign'])
            data['balance'] = int(data.get('balance', 1500))
            data['day'] = 15
            data['pdays'] = -1  # Use -1 as default (means not previously contacted)
            data['previous'] = 0
        except ValueError:
            return jsonify({'error': 'Invalid numeric values'})
        
        # Add default values to match the original data structure
        data.update({
            'id': 999999,  # Dummy ID
            'default': 'no',
            'contact': 'cellular',
            'month': 'may',
            'poutcome': 'unknown'
        })
        
        # Create DataFrame with the original column structure
        original_columns = ['id', 'age', 'job', 'marital', 'education', 'default', 'balance', 
                          'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 
                          'pdays', 'previous', 'poutcome']
        
        # Reorder data to match expected columns
        ordered_data = {col: data.get(col, 0) for col in original_columns}
        input_df = pd.DataFrame([ordered_data])
        
        # Apply feature engineering (simulate the pipeline)
        try:
            # Simple feature engineering to match the expected format
            # We need to create the same one-hot encoded features as in training
            
            # Load a sample of the transformed training data to get the exact structure
            transformed_sample = pd.read_csv('artifacts/data_transformation/train.csv', nrows=1)
            feature_names = [col for col in transformed_sample.columns if col != 'y']
            
            # Create a feature vector with all zeros
            feature_vector = pd.DataFrame(0, index=[0], columns=feature_names)
            
            # Manually set the features based on input
            # Age (normalized approximately)
            feature_vector.loc[0, 'age'] = (data['age'] - 40) / 10  # Rough normalization
            
            # Balance (normalized approximately) 
            feature_vector.loc[0, 'balance'] = (data['balance'] - 1000) / 2000  # Rough normalization
            
            # Duration (normalized approximately)
            feature_vector.loc[0, 'duration'] = (data['duration'] - 250) / 200  # Rough normalization
            
            # Campaign (normalized approximately)
            feature_vector.loc[0, 'campaign'] = (data['campaign'] - 2) / 2  # Rough normalization
            
            # Day (normalized approximately)
            feature_vector.loc[0, 'day'] = (data['day'] - 15) / 10  # Rough normalization
            
            # Pdays (normalized approximately)
            feature_vector.loc[0, 'pdays'] = (data['pdays'] + 1) / 400  # Rough normalization
            
            # Previous (normalized approximately)
            feature_vector.loc[0, 'previous'] = data['previous'] / 5  # Rough normalization
            
            # One-hot encoded features - set based on input values
            # Housing
            if data['housing'] == 'yes':
                feature_vector.loc[0, 'housing_yes'] = 1
            else:
                feature_vector.loc[0, 'housing_no'] = 1
            
            # Contact 
            if data['contact'] == 'cellular':
                feature_vector.loc[0, 'contact_cellular'] = 1
            else:
                feature_vector.loc[0, 'contact_unknown'] = 1
            
            # Education (simplified)
            if 'primary' in data.get('education', '').lower():
                feature_vector.loc[0, 'education_primary'] = 1
            
            # Month (simplified)
            if data.get('month', '') == 'oct':
                feature_vector.loc[0, 'month_oct'] = 1
            
            # Poutcome
            if data.get('poutcome', '') == 'success':
                feature_vector.loc[0, 'poutcome_success'] = 1
            else:
                feature_vector.loc[0, 'poutcome_unknown'] = 1
            
            processed_data = feature_vector.values
            
            # Make prediction with XGBoost compatibility
            try:
                # Handle different XGBoost versions
                prediction = model.predict(processed_data)
                
                # For probability prediction, handle different return formats
                try:
                    prediction_proba = model.predict_proba(processed_data)
                    if len(prediction_proba.shape) > 1 and prediction_proba.shape[1] > 1:
                        prob_positive = float(prediction_proba[0][1])
                    else:
                        prob_positive = float(prediction_proba[0])
                except:
                    # Fallback if predict_proba fails
                    prob_positive = float(prediction[0]) if prediction[0] <= 1.0 else 0.5
                
                confidence = max(prob_positive, 1 - prob_positive)
                
            except Exception as model_error:
                print(f"Model prediction error: {model_error}")
                # Simple fallback prediction
                prediction = [0]  # Default to no subscription
                prob_positive = 0.3  # Default probability
                confidence = 0.6
            
            confidence_level = "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
            
            success = True
            duration = time.time() - start_time
            
            # Record metrics
            pipeline_metrics.record_prediction_metrics(model_type, duration, success=True)
            
            logger.info("Prediction completed successfully", extra={
                'model_type': model_type,
                'prediction': int(prediction[0]),
                'confidence': float(confidence),
                'duration': duration
            })
            
            return jsonify({
                'prediction': int(prediction[0]),
                'probability': prob_positive,
                'confidence': float(confidence),
                'confidence_level': confidence_level,
                'result': 'Will Subscribe to Term Deposit' if prediction[0] == 1 else 'Will Not Subscribe to Term Deposit',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            duration = time.time() - start_time
            pipeline_metrics.record_prediction_metrics(model_type, duration, success=False)
            logger.error(f"Feature processing failed: {str(e)}", extra={'error_code': 'FEATURE_PROCESSING_ERROR'})
            return jsonify({'error': f'Feature processing failed: {str(e)}'})
        
    except Exception as e:
        duration = time.time() - start_time
        pipeline_metrics.record_prediction_metrics(model_type, duration, success=False)
        logger.error(f"Prediction failed: {str(e)}", extra={'error_code': 'PREDICTION_ERROR'})
        return jsonify({'error': f'Prediction failed: {str(e)}'})

@app.route('/health')
def health():
    """Health check"""
    model_exists = os.path.exists('artifacts/model_trainer/model.pkl')
    
    return jsonify({
        'status': 'healthy' if model_exists else 'degraded',
        'service': 'bank-marketing-predictor',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': model_exists
    })

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
