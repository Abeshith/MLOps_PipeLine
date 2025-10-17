from prometheus_client import Counter, Gauge, Histogram, start_http_server, REGISTRY
import threading
import time
import psutil
import os

class PipelineMetrics:
    def __init__(self):
        # Counters - for counting events that happen in the pipeline
        self.data_ingestion_counter = Counter(
            'ml_data_ingestion_total', 
            'Total number of data ingestion operations completed'
        )
        
        self.data_ingestion_failures_counter = Counter(
            'ml_data_ingestion_failures_total',
            'Total number of data ingestion failures'
        )
        
        self.feature_engineering_counter = Counter(
            'ml_feature_engineering_total', 
            'Total number of feature engineering operations completed'
        )
        
        self.feature_engineering_failures_counter = Counter(
            'ml_feature_engineering_failures_total',
            'Total number of feature engineering failures'
        )
        
        self.model_training_counter = Counter(
            'ml_model_training_total', 
            'Total number of model training operations completed'
        )
        
        self.model_training_failures_counter = Counter(
            'ml_model_training_failures_total',
            'Total number of model training failures'
        )
        
        self.model_prediction_counter = Counter(
            'ml_model_predictions_total',
            'Total number of model predictions made',
            ['model_type', 'status']
        )
        
        self.data_validation_counter = Counter(
            'ml_data_validation_total',
            'Total number of data validation operations'
        )
        
        self.data_transformation_counter = Counter(
            'ml_data_transformation_total',
            'Total number of data transformation operations'
        )
        
        # Gauges - for values that can go up and down
        self.data_size_gauge = Gauge(
            'ml_data_size', 
            'Current size of processed dataset (number of rows)'
        )
        
        self.model_accuracy_gauge = Gauge(
            'ml_model_accuracy', 
            'Current model accuracy score (0.0 to 1.0)'
        )
        
        self.model_precision_gauge = Gauge(
            'ml_model_precision',
            'Current model precision score (0.0 to 1.0)'
        )
        
        self.model_recall_gauge = Gauge(
            'ml_model_recall',
            'Current model recall score (0.0 to 1.0)'
        )
        
        self.model_f1_gauge = Gauge(
            'ml_model_f1_score',
            'Current model F1 score (0.0 to 1.0)'
        )
        
        self.feature_count_gauge = Gauge(
            'ml_feature_count',
            'Number of features in the current dataset'
        )
        
        self.training_data_size_gauge = Gauge(
            'ml_training_data_size',
            'Size of training dataset (number of rows)'
        )
        
        self.test_data_size_gauge = Gauge(
            'ml_test_data_size',
            'Size of test dataset (number of rows)'
        )
        
        # System metrics
        self.cpu_usage_gauge = Gauge(
            'ml_system_cpu_usage_percent',
            'Current CPU usage percentage'
        )
        
        self.memory_usage_gauge = Gauge(
            'ml_system_memory_usage_percent',
            'Current memory usage percentage'
        )
        
        self.disk_usage_gauge = Gauge(
            'ml_system_disk_usage_percent',
            'Current disk usage percentage'
        )
        
        # Histograms - for timing operations
        self.training_duration_histogram = Histogram(
            'ml_training_duration_seconds',
            'Time spent training models',
            buckets=[1, 5, 10, 30, 60, 300, 600, 1800, 3600, 7200]
        )
        
        self.prediction_duration_histogram = Histogram(
            'ml_prediction_duration_seconds',
            'Time spent making predictions',
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
        )
        
        self.data_processing_duration_histogram = Histogram(
            'ml_data_processing_duration_seconds',
            'Time spent processing data',
            buckets=[1, 5, 10, 30, 60, 300, 600, 1800]
        )

    def start_metrics_server(self, port=8000):
        """Start Prometheus metrics server in a separate thread"""
        def start_server():
            try:
                start_http_server(port)
                print(f"✅ Metrics server started on port {port}")
                self._start_system_metrics_collection()
            except Exception as e:
                print(f"❌ Failed to start metrics server: {e}")
        
        metrics_thread = threading.Thread(target=start_server, daemon=True)
        metrics_thread.start()
    
    def _start_system_metrics_collection(self):
        """Start collecting system metrics in background"""
        def collect_system_metrics():
            while True:
                try:
                    # CPU usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    self.cpu_usage_gauge.set(cpu_percent)
                    
                    # Memory usage
                    memory = psutil.virtual_memory()
                    self.memory_usage_gauge.set(memory.percent)
                    
                    # Disk usage
                    disk = psutil.disk_usage('/')
                    disk_percent = (disk.used / disk.total) * 100
                    self.disk_usage_gauge.set(disk_percent)
                    
                    time.sleep(10)  # Update every 10 seconds
                except Exception as e:
                    print(f"Error collecting system metrics: {e}")
                    time.sleep(30)
        
        system_thread = threading.Thread(target=collect_system_metrics, daemon=True)
        system_thread.start()
    
    def record_training_metrics(self, accuracy, precision, recall, f1_score, duration):
        """Record model training metrics"""
        self.model_accuracy_gauge.set(accuracy)
        self.model_precision_gauge.set(precision)
        self.model_recall_gauge.set(recall)
        self.model_f1_gauge.set(f1_score)
        self.training_duration_histogram.observe(duration)
        self.model_training_counter.inc()
    
    def record_prediction_metrics(self, model_type, duration, success=True):
        """Record prediction metrics"""
        status = 'success' if success else 'failure'
        self.model_prediction_counter.labels(model_type=model_type, status=status).inc()
        self.prediction_duration_histogram.observe(duration)
    
    def record_data_metrics(self, train_size, test_size, feature_count):
        """Record data-related metrics"""
        self.training_data_size_gauge.set(train_size)
        self.test_data_size_gauge.set(test_size)
        self.feature_count_gauge.set(feature_count)
        self.data_size_gauge.set(train_size + test_size)
    
    def increment_failure_counter(self, operation):
        """Increment failure counters for different operations"""
        if operation == 'data_ingestion':
            self.data_ingestion_failures_counter.inc()
        elif operation == 'feature_engineering':
            self.feature_engineering_failures_counter.inc()
        elif operation == 'model_training':
            self.model_training_failures_counter.inc()

pipeline_metrics = PipelineMetrics()
