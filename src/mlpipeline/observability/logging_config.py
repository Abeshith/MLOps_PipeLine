import logging
import json
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'process_id': os.getpid(),
            'thread_id': record.thread,
            'pipeline_stage': getattr(record, 'pipeline_stage', 'unknown'),
            'component': getattr(record, 'component', 'unknown')
        }
        
        # Add custom fields if they exist
        if hasattr(record, 'model_accuracy'):
            log_entry['model_accuracy'] = record.model_accuracy
        if hasattr(record, 'data_size'):
            log_entry['data_size'] = record.data_size
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration
        if hasattr(record, 'error_code'):
            log_entry['error_code'] = record.error_code
            
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            log_entry['exception_type'] = record.exc_info[0].__name__ if record.exc_info[0] else None
            
        return json.dumps(log_entry)

class PipelineLoggerAdapter(logging.LoggerAdapter):
    """Custom logger adapter for ML pipeline context"""
    
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})
    
    def process(self, msg, kwargs):
        # Add pipeline context to all log messages
        kwargs.setdefault('extra', {}).update(self.extra)
        return msg, kwargs

def setup_logging(log_level=logging.INFO, log_dir='logs'):
    """Setup comprehensive logging for ML pipeline"""
    
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # JSON formatter for structured logs
    json_formatter = JSONFormatter()
    
    # Console formatter for human-readable logs
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(component)s:%(pipeline_stage)s] - %(message)s',
        defaults={'component': 'unknown', 'pipeline_stage': 'unknown'}
    )
    
    # Rotating file handler for JSON logs (for ELK stack)
    json_file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'ml_pipeline.json'),
        maxBytes=50*1024*1024,  # 50MB
        backupCount=5
    )
    json_file_handler.setFormatter(json_formatter)
    json_file_handler.setLevel(log_level)
    
    # Rotating file handler for text logs (for debugging)
    text_file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'ml_pipeline.log'),
        maxBytes=50*1024*1024,  # 50MB
        backupCount=5
    )
    text_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    ))
    text_file_handler.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    
    # Error file handler (errors only)
    error_file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=3
    )
    error_file_handler.setFormatter(json_formatter)
    error_file_handler.setLevel(logging.ERROR)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add all handlers
    root_logger.addHandler(json_file_handler)
    root_logger.addHandler(text_file_handler)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_file_handler)
    
    return root_logger

def get_pipeline_logger(name, component='unknown', pipeline_stage='unknown'):
    """Get a logger with pipeline context"""
    logger = logging.getLogger(name)
    return PipelineLoggerAdapter(logger, {
        'component': component,
        'pipeline_stage': pipeline_stage
    })

# Configure different loggers for different components
def setup_component_loggers():
    """Setup specialized loggers for different pipeline components"""
    
    # Data ingestion logger
    data_ingestion_logger = get_pipeline_logger(
        'mlpipeline.data_ingestion',
        component='data_ingestion',
        pipeline_stage='ingestion'
    )
    
    # Feature engineering logger
    feature_engineering_logger = get_pipeline_logger(
        'mlpipeline.feature_engineering',
        component='feature_engineering',
        pipeline_stage='feature_engineering'
    )
    
    # Model training logger
    model_training_logger = get_pipeline_logger(
        'mlpipeline.model_training',
        component='model_training',
        pipeline_stage='training'
    )
    
    # Model evaluation logger
    model_evaluation_logger = get_pipeline_logger(
        'mlpipeline.model_evaluation',
        component='model_evaluation',
        pipeline_stage='evaluation'
    )
    
    # Prediction logger
    prediction_logger = get_pipeline_logger(
        'mlpipeline.prediction',
        component='prediction',
        pipeline_stage='prediction'
    )
    
    return {
        'data_ingestion': data_ingestion_logger,
        'feature_engineering': feature_engineering_logger,
        'model_training': model_training_logger,
        'model_evaluation': model_evaluation_logger,
        'prediction': prediction_logger
    }

# Initialize logging
setup_logging()
component_loggers = setup_component_loggers()
