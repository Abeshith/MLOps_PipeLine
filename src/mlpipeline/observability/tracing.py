import functools
import time
import logging

# Setup logging for tracing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTracer:
    """Simplified tracer for basic function tracing without external dependencies"""
    
    def __init__(self, service_name='ml-pipeline'):
        self.service_name = service_name
        self.enabled = True
    
    def start_span(self, span_name):
        """Create a simple span context for timing and logging"""
        return SimpleSpan(span_name, self.service_name)

class SimpleSpan:
    """Simple span implementation for basic tracing"""
    
    def __init__(self, name, service_name):
        self.name = name
        self.service_name = service_name
        self.start_time = None
        self.tags = {}
        
    def __enter__(self):
        self.start_time = time.time()
        logger.info(f"[TRACE] Starting span: {self.name} in service: {self.service_name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        if exc_type is not None:
            self.tags['error'] = True
            self.tags['error_message'] = str(exc_val)
            logger.error(f"[TRACE] Span {self.name} failed after {duration:.2f}s - Error: {exc_val}")
        else:
            self.tags['success'] = True
            logger.info(f"[TRACE] Completed span: {self.name} in {duration:.2f}s")
    
    def set_tag(self, key, value):
        """Set tag on span"""
        self.tags[key] = value

# Global tracer instance
tracer = SimpleTracer()

def trace_function(func):
    """
    Decorator to trace function execution with timing and error handling
    Used in: data_ingestion.py, feature_engineering.py, data_transformation.py, 
             model_trainer.py, model_evaluation.py, app.py
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with tracer.start_span(func.__name__) as span:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                span.set_tag('success', True)
                return result
            except Exception as e:
                span.set_tag('error', True)
                span.set_tag('error.message', str(e))
                raise
            finally:
                duration = time.time() - start_time
                span.set_tag('duration', duration)
                logger.info(f"Function {func.__name__} executed in {duration:.2f} seconds")
    return wrapper

# Optional: Jaeger integration (requires jaeger-client package)
def init_jaeger_tracer(service_name='ml-pipeline'):
    """
    Initialize Jaeger tracer if jaeger-client is available
    This is optional and the pipeline will work with SimpleTracer if Jaeger is not available
    """
    try:
        from jaeger_client import Config
        
        config = Config(
            config={
                'sampler': {
                    'type': 'const',
                    'param': 1,
                },
                'local_agent': {
                    'reporting_host': 'localhost',
                    'reporting_port': 6831,
                },
                'logging': True,
            },
            service_name=service_name,
            validate=True,
        )
        return config.initialize_tracer()
    except ImportError:
        logger.warning("jaeger-client not available, using SimpleTracer")
        return SimpleTracer(service_name)
    except Exception as e:
        logger.warning(f"Failed to initialize Jaeger tracer: {e}, using SimpleTracer")
        return SimpleTracer(service_name)

tracer = init_jaeger_tracer()
