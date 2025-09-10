#!/usr/bin/env python3
"""
Simple validation script for the MLOps pipeline
"""

import requests
import time
import sys
import json

def test_health_endpoint(base_url="http://localhost:5000"):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed with error: {e}")
        return False

def test_prediction_endpoint(base_url="http://localhost:5000"):
    """Test the prediction endpoint with sample data"""
    try:
        # Sample data for testing
        sample_data = {
            "age": 35,
            "job": "management",
            "marital": "married",
            "education": "tertiary",
            "default": "no",
            "balance": 1500,
            "housing": "yes",
            "loan": "no",
            "contact": "cellular",
            "day": 15,
            "month": "may",
            "duration": 200,
            "campaign": 1,
            "pdays": -1,
            "previous": 0,
            "poutcome": "unknown"
        }
        
        response = requests.post(
            f"{base_url}/predict", 
            json=sample_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction endpoint working")
            print(f"   Sample prediction: {result}")
            return True
        else:
            print(f"❌ Prediction endpoint failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction endpoint failed with error: {e}")
        return False

def test_metrics_endpoint(base_url="http://localhost:8000"):
    """Test the metrics endpoint"""
    try:
        response = requests.get(f"{base_url}/metrics", timeout=10)
        if response.status_code == 200:
            print("✅ Metrics endpoint working")
            return True
        else:
            print(f"❌ Metrics endpoint failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Metrics endpoint failed with error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting MLOps Pipeline Validation...")
    
    # Wait for application to start
    print("⏳ Waiting for application to start...")
    time.sleep(5)
    
    tests_passed = 0
    total_tests = 3
    
    # Test health endpoint
    if test_health_endpoint():
        tests_passed += 1
    
    # Test prediction endpoint
    if test_prediction_endpoint():
        tests_passed += 1
    
    # Test metrics endpoint
    if test_metrics_endpoint():
        tests_passed += 1
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! MLOps Pipeline is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()
