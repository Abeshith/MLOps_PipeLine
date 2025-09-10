import sys
from mlpipeline import logger

def error_message_detail(error, error_detail: sys):
    """
    Extract detailed error information
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"
    
    return error_message

class CustomException(Exception):
    """
    Custom Exception class for ML Pipeline
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message

# Data Processing Exceptions
class DataIngestionException(CustomException):
    """Exception raised for data ingestion errors"""
    pass

class DataValidationException(CustomException):
    """Exception raised for data validation errors"""
    pass

class FeatureEngineeringException(CustomException):
    """Exception raised for feature engineering errors"""
    pass

class DataTransformationException(CustomException):
    """Exception raised for data transformation errors"""
    pass

class ModelTrainingException(CustomException):
    """Exception raised for model training errors"""
    pass

class ModelEvaluationException(CustomException):
    """Exception raised for model evaluation errors"""
    pass

class ModelDeploymentException(CustomException):
    """Exception raised for model deployment errors"""
    pass

# Configuration Exceptions
class ConfigurationException(CustomException):
    """Exception raised for configuration errors"""
    pass

# File Operation Exceptions
class FileOperationException(CustomException):
    """Exception raised for file operation errors"""
    pass

# Simple usage example
if __name__ == "__main__":
    try:
        # Simulate an error
        a = 1/0
    except Exception as e:
        logger.info("Testing custom exception")
        raise CustomException(e, sys)
