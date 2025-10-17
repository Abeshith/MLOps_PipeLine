<div align="center">

# MACHINE LEARNING OPERATIONS PIPELINE

![last commit](https://img.shields.io/github/last-commit/Abeshith/MLOps_PipeLine?color=blue&label=last%20commit&style=flat)
![Python](https://img.shields.io/badge/python-84.2%25-blue&style=flat)
![Languages](https://img.shields.io/badge/languages-4-lightgrey&style=flat)

## Built with the tools and technologies:

![Flask](https://img.shields.io/badge/Flask-black?style=flat&logo=flask&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-black?style=flat&logo=json&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-black?style=flat&logo=markdown&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-red?style=flat&logo=yaml&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-orange?style=flat&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-orange?style=flat&logo=xgboost&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-blue?style=flat&logo=dvc&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-blue?style=flat&logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-purple?style=flat&logo=pandas&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-lightblue?style=flat&logo=kaggle&logoColor=white)

![MLflow](https://img.shields.io/badge/MLflow-blue?style=flat&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-blue?style=flat&logo=kubernetes&logoColor=white)
![Python](https://img.shields.io/badge/Python-blue?style=flat&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-blue?style=flat&logo=apache-airflow&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-blue?style=flat&logo=github-actions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-orange?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-orange?style=flat&logo=grafana&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-yellow?style=flat&logo=elasticsearch&logoColor=white)

</div>

---

## 📊 **Production-Ready Observability Stack**

### **🔍 Complete Monitoring Integration**
- **Single Production App**: `production_app.py` - Unified Flask application with built-in observability
- **15+ ML Metrics**: Model performance, prediction analytics, system health monitoring
- **Structured Logging**: Request tracing with Elasticsearch integration
- **Real-time Dashboards**: Grafana visualizations for ML pipeline insights
- **Health Monitoring**: Comprehensive endpoint monitoring and alerting

### **📈 Observability Components**
- 🎯 **Prometheus**: 15+ custom ML metrics (accuracy, confidence, error rates, latency)
- 📊 **Grafana**: Production dashboards for model performance and business KPIs
- 🔍 **Elasticsearch + Kibana**: Centralized logging with request tracing and error analysis
- 🚨 **AlertManager**: Automated alerts for model degradation and system issues
- 📋 **Health Endpoints**: `/health`, `/status`, `/metrics` for comprehensive monitoring

### **🎯 Key Monitoring Metrics**
```
Model Performance: ml_model_accuracy, ml_model_precision, ml_model_recall
Prediction Analytics: ml_predictions_by_class, ml_prediction_confidence
System Health: ml_prediction_error_rate, http_request_duration_seconds
Business KPIs: prediction distribution, confidence trends, response times
```

## � About the Project & Approach

This repository demonstrates a **comprehensive MLOps (Machine Learning Operations) pipeline** that showcases industry-standard practices for end-to-end machine learning workflow automation. The project implements a production-ready ML system with automated training, validation, deployment, and monitoring capabilities.

### 🎯 Project Approach

This MLOps pipeline follows a **modular, scalable architecture** designed to handle real-world machine learning challenges:

1. **Data-Centric Approach**: Implements robust data ingestion, validation, and feature engineering processes
2. **Model-Centric Operations**: Automated model training, evaluation, and deployment with performance tracking
3. **Infrastructure-as-Code**: Kubernetes manifests and Docker containerization for scalable deployments
4. **Observability-First**: Comprehensive monitoring with metrics, logs, and distributed tracing
5. **CI/CD Integration**: Automated testing, security scanning, and deployment pipelines

### � What I Built

**Core ML Pipeline Components:**
- � **6-Stage DVC Pipeline**: Data ingestion → Validation → Feature engineering → Transformation → Training → Evaluation
- 🤖 **XGBoost Model**: Achieved 92.15% accuracy with automated hyperparameter tuning
- 📊 **MLflow Integration**: Experiment tracking and model registry for version control
- 🔍 **Data Quality Monitoring**: Evidently AI for drift detection and quality assessment

**Production Infrastructure:**
- 🐳 **Docker Containerization**: Multi-stage builds with security best practices
- ☸️ **Kubernetes Deployment**: Scalable orchestration with services, ingress, and monitoring
- 🌪️ **Apache Airflow**: Workflow orchestration and scheduling for automated pipeline execution
- 🚀 **GitHub Actions CI/CD**: Automated testing, security scanning, and deployment

**Observability Stack:**
- 📈 **Prometheus**: Metrics collection and alerting for model performance
- 📊 **Grafana**: Custom dashboards for ML pipeline visualization
- 🔍 **ELK Stack**: Centralized logging with Elasticsearch, Kibana, and Fluentd
- 🕸️ **Jaeger**: Distributed tracing for microservices monitoring

---

##  Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git & DVC
- Kaggle Account (for data access)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Abeshith/MLOps_PipeLine.git
cd MLOps_PipeLine
```

2. **Set up Python environment**
```bash
# Using uv (recommended)
uv venv
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

3. **Configure Kaggle credentials**
```bash
# Create kaggle.json in ~/.kaggle/ directory
{
  "username": "your_kaggle_username",
  "key": "your_kaggle_key"
}
```

---

## 🔄 Pipeline Execution

### Individual Stage Execution

**Stage 1: Data Ingestion**
```bash
python -m src.mlpipeline.pipeline.stage_01_data_ingestion

or 

$env:PYTHONPATH = "src"; python src/mlpipeline/pipeline/stage_01_data_ingestion.py                


```
*Downloads Kaggle competition data, splits into train/test sets, validates data integrity*

**Stage 2: Data Validation**
```bash
python -m src.mlpipeline.pipeline.stage_02_data_validation

or 

$env:PYTHONPATH = "src"; python src/mlpipeline/pipeline/stage_02_data_validation.py                

```
*Schema validation against config/schema.yaml, data drift detection using Evidently AI*

**Stage 3: Feature Engineering**
```bash
python -m src.mlpipeline.pipeline.stage_03_feature_engineering

or

$env:PYTHONPATH = "src"; python src/mlpipeline/pipeline/stage_03_feature_engineering.py      
```
*Feature creation and transformation, correlation analysis, feature importance calculation*

**Stage 4: Data Transformation**
```bash
python -m src.mlpipeline.pipeline.stage_04_data_transformation

or  

$env:PYTHONPATH = "src"; python src/mlpipeline/pipeline/stage_04_data_transformation.py                

```
*Data preprocessing and scaling, encoding categorical variables, train/test preparation*

**Stage 5: Model Training**
```bash
python -m src.mlpipeline.pipeline.stage_05_model_trainer

or 

$env:PYTHONPATH = "src"; python src/mlpipeline/pipeline/stage_05_model_trainer.py                
```
*XGBoost model training with hyperparameter tuning, MLflow experiment tracking*

**Stage 6: Model Evaluation**
```bash
python -m src.mlpipeline.pipeline.stage_06_model_evaluation

or

$env:PYTHONPATH = "src"; python src/mlpipeline/pipeline/stage_06_model_evaluation.py                            
```
*Performance metrics calculation, model comparison, results logging to MLflow*

### Complete Pipeline Execution

**Run Complete Pipeline Script**
```bash
python main.py

or

$env:PYTHONPATH = "src"; python main.py
```
*Executes all 6 stages sequentially with comprehensive logging and error handling*

**Start Flask Application**
```bash
python app.py

or 

$env:PYTHONPATH = "src"; python main.py
```
*Launches web interface at http://localhost:5000 for model predictions and monitoring*

### DVC Pipeline Management

```bash
# Run complete pipeline
dvc repro

# Run specific stages
dvc repro data_ingestion
dvc repro data_validation
dvc repro feature_engineering
dvc repro data_transformation
dvc repro model_trainer
dvc repro model_evaluation

# View pipeline status
dvc dag
```

---

## ⚡ Apache Airflow Pipeline Setup

**Prerequisites**
> Note: Apache Airflow requires Linux-based systems for optimal performance. Windows users should use WSL or Linux environment.

### Environment Setup

**1. Copy Project to Linux Environment (Windows Users)**
```bash
cp -r /mnt/d/MLOps_PipeLine ~/
```

**2. Install Python and Setup Virtual Environment**
```bash
# Install Python3 if not already installed
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Navigate to project directory
cd ~/MLOps_PipeLine

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**3. Configure Apache Airflow**
```bash
# Set Airflow home directory
export AIRFLOW_HOME=~/airflow
echo $AIRFLOW_HOME

# Configure Airflow settings
vim ~/airflow/airflow.cfg

-> insert - i
Replace "auth_manager = airflow.api.fastapi.auth.managers.simple.simple_auth_manager.SimpleAuthManager" in airflow.cfg file
with "auth_manager=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager".
After Updation press- > esc -> :wq!

# Create DAGs directory
mkdir -p ~/airflow/dags

# Copy DAG file to Airflow directory
cp model_dag.py ~/airflow/dags/

# Test DAG configuration
python ~/airflow/dags/model_dag.py
```

**4. Launch Airflow Webserver**
```bash
# Start Airflow standalone mode
airflow standalone
```

**5. Execute Pipeline**
- Open your web browser and navigate to: **http://0.0.0.0:8080**
- Search for **ml_pipeline_dag** in the DAGs list
- Click on the DAG and trigger the pipeline execution
- Monitor the workflow progress through the Airflow UI

---

## ☸️ Kubernetes Deployment

### **1. Start Minikube Cluster**
```bash
# Initialize Minikube cluster
minikube start
```

### **2. Deploy Application**
```bash
# Deploy the application using deployment manifest
kubectl apply -f k8s/deployment.yaml

# Check pod status
kubectl get pods
```

### **3. Deploy Services**
```bash
# Apply service configuration
kubectl apply -f k8s/service.yaml

# Verify service deployment
kubectl get svc
```

### **4. Access Application - Method 1 (Port Forwarding)**
```bash
# Forward service port to local machine
kubectl port-forward svc/mlapp-service 8000:80

# Access application in browser
# Navigate to: http://localhost:8000
```

### **5. Access Application - Method 2 (Load Balancer)**
```bash
# Edit service configuration
kubectl edit svc mlapp-service

# Change service type from NodePort to LoadBalancer
esc - :wq! - enter
# Save and exit the editor

# Open new terminal and create tunnel
minikube tunnel

# In original terminal, check for external IP
kubectl get svc

# Access application using external IP in browser
# 127.0.0.1
```

### **6. Configuring Ingress - (Optional)**
```bash
# Deploy the ingress.yaml file
kubectl apply -f k8s/ingress.yaml

# Install the Ingress Controller (nginx)
minikube addons enable ingress

# Check the downloaded Ingress
kubectl get pods -A | grep nginx

# Check Ingress is Deployed
kubectl get ingress # A Address is Being Updated like -> 192.168.49.2

# for setup local system configuraton
sudo vim /etc/hosts

# Add
127.0.0.1       localhost
127.0.1.1       Abis-PC.        Abis-PC
192.168.49.2    foo.bar.com
esc - :wq!

# Check Updated or not
ping foo.bar.com

# then go to browser
http://foo.bar.com/demo
http://foo.bar.com/admin
```

---

## 📊 Observability Stack

### 🔍 **Metrics Collection with Prometheus**

**Start Prometheus Monitoring**
```bash
# Navigate to observability directory
cd observability

# Start Prometheus service
docker-compose up -d prometheus

# Access Prometheus UI
# URL: http://localhost:9090
```

**Prometheus Operations**
```bash
# Check application health
curl http://localhost:9090/api/v1/query?query=up

# View custom metrics
curl http://localhost:9090/api/v1/query?query=ml_model_accuracy

# Check targets status
curl http://localhost:9090/api/v1/targets

# View alert rules
curl http://localhost:9090/api/v1/rules
```

**Configure ML Pipeline Metrics**
```bash
# Prometheus collects metrics for:
# - Model accuracy and performance
# - Pipeline execution times
# - Resource utilization
# - API response times
# - Error rates and failures
```

### 📈 **Visualization with Grafana**

**Start Grafana Dashboard**
```bash
# Start Grafana service
docker-compose up -d grafana

# Access Grafana UI
# URL: http://localhost:3000
# Default credentials: admin/admin
```

**Import ML Pipeline Dashboards**
```bash
# Pre-configured dashboards available:
# 1. ML Pipeline Performance Dashboard
# 2. Model Metrics Dashboard  
# 3. Infrastructure Monitoring Dashboard

# Import custom dashboard JSON files from:
# observability/grafana/dashboards/
```

**Grafana Operations**
```bash
# Create data source (Prometheus)
# URL: http://prometheus:9090

# Import dashboard from file
# Upload: observability/grafana/dashboards/ml-pipeline-dashboard.json

# Set up alerting rules for model performance
# Configure notification channels (email, slack, webhook)
```

### 📋 **Log Management with ELK Stack**

**Start Elasticsearch & Kibana**
```bash
# Start Elasticsearch service
docker-compose up -d elasticsearch

# Start Kibana service  
docker-compose up -d kibana

# Access Kibana UI
# URL: http://localhost:5601
```

**Elasticsearch Operations**
```bash
# Check cluster health
curl http://localhost:9200/_cluster/health

# List indices
curl http://localhost:9200/_cat/indices?v

# Search ML pipeline logs
curl -X GET "localhost:9200/logs-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "level": "ERROR"
    }
  }
}'

# View pipeline execution logs
curl -X GET "localhost:9200/ml-pipeline-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1h"
      }
    }
  }
}'
```

**Kibana Dashboard Setup**
```bash
# Create index patterns for:
# - ml-pipeline-* (Pipeline execution logs)
# - application-* (Application logs)
# - error-* (Error logs)
# - performance-* (Performance metrics)

# Build visualizations for:
# - Pipeline success/failure rates
# - Model training duration trends
# - Error analysis and patterns
# - Resource usage over time
```

**Fluentd Log Collection**
```bash
# Start Fluentd service
docker-compose up -d fluentd

# Fluentd automatically collects logs from:
# - ML pipeline stages
# - Flask application
# - Kubernetes pods (if deployed)
# - Docker containers
# - System logs

# Configure log parsing in:
# observability/fluentd/fluent.conf
```

### 🕸️ **Distributed Tracing with Jaeger**

**Start Jaeger Tracing**
```bash
# Start Jaeger service
docker-compose up -d jaeger

# Access Jaeger UI
# URL: http://localhost:16686
```

**Jaeger Operations**
```bash
# View ML pipeline traces
# Search for service: ml-pipeline
# View operation: model_training

# Analyze request flows:
# - Data ingestion → validation → training → evaluation
# - API request → prediction → response
# - Error traces and bottleneck identification

# Configure trace sampling and retention
# Monitor microservice dependencies
```

### 🚨 **Alerting & Monitoring**

**Complete Monitoring Stack**
```bash
# Start all monitoring services
docker-compose up -d

# Check services status
docker-compose ps

# View service logs
docker-compose logs prometheus
docker-compose logs grafana
docker-compose logs elasticsearch
```

**Alert Configuration**
```bash
# Prometheus alerts configured for:
# - Model accuracy degradation (< 90%)
# - High error rates (> 5%)
# - Pipeline failures
# - Resource exhaustion
# - API latency issues

# View active alerts
# URL: http://localhost:9090/alerts

# Configure alert notifications in Grafana
# Set up escalation policies and on-call rotations
```

**Monitoring Cleanup**
```bash
# Stop all services
docker-compose down

# Remove volumes (caution: deletes all data)
docker-compose down -v

# Remove specific service
docker-compose stop grafana
docker-compose rm grafana
```

---

## 🔄 CI/CD Pipeline

**Automated MLOps pipeline with GitHub Actions**

### Pipeline Stages:

1. **Setup**: Python environment and dependencies
2. **Code Quality**: Black formatting, isort, flake8 linting  
3. **Data Validation**: Schema validation and data quality checks
4. **Model Performance**: Accuracy threshold validation (>90%)
5. **Security Scan**: Secret detection and vulnerability scanning
6. **Build & Deploy**: Docker build and push to registry

### Triggers:
- Push to `main` branch
- Pull request creation  
- Manual workflow dispatch

### Required Secrets:
```bash
# Add to GitHub repository secrets:
DOCKER_USERNAME=your_docker_username
DOCKER_PASSWORD=your_docker_password
```

---

## 🔧 **Complete Observability Implementation**

### **🚀 Production Application**
```bash
# Start the unified production application
python production_app.py

# Available endpoints:
http://localhost:5000/predict   # ML predictions with monitoring
http://localhost:5000/health    # Health check endpoint  
http://localhost:5000/status    # Detailed system status
http://localhost:5000/metrics   # Prometheus metrics
```

### **📊 Monitoring Stack**
```bash
# Start complete observability stack
cd observability
docker compose up -d

# Access monitoring tools:
http://localhost:9090   # Prometheus (Metrics)
http://localhost:3000   # Grafana (Dashboards) 
http://localhost:9200   # Elasticsearch (Logs)
http://localhost:5601   # Kibana (Log Analysis)
```

### **🎯 Key Features**
- **15+ ML Metrics**: Model performance, prediction analytics, system health
- **Structured Logging**: Request tracing with Elasticsearch integration
- **Real-time Dashboards**: Grafana visualizations for ML insights
- **Health Monitoring**: Comprehensive endpoint monitoring
- **Error Tracking**: Detailed error logging and alerting

### **📈 Available Metrics**
```
Model Performance: ml_model_accuracy, ml_model_precision, ml_model_recall
Prediction Analytics: ml_predictions_by_class, ml_prediction_confidence  
System Health: ml_prediction_error_rate, http_request_duration_seconds
Business KPIs: prediction distribution, confidence trends, response times
```

**📋 For detailed setup instructions, see [Observability.md](Observability.md)**

---

## � Project Structure

```
MLOps_PipeLine/
├── 📂 src/mlpipeline/           # Core ML pipeline source code
│   ├── 📂 components/           # ML pipeline components
│   ├── 📂 config/              # Configuration management
│   ├── 📂 entity/              # Data entities and schemas
│   ├── 📂 pipeline/            # Stage-wise pipeline execution
│   └── 📂 utils/               # Utility functions
├── 📂 config/                   # Configuration files
│   ├── config.yaml             # Main configuration
│   ├── params.yaml             # Model parameters
│   └── schema.yaml             # Data schema validation
├── 📂 artifacts/               # Generated artifacts (DVC tracked)
│   ├── 📂 data_ingestion/      # Raw and processed data
│   ├── 📂 data_validation/     # Validation reports
│   ├── 📂 feature_engineering/ # Feature artifacts
│   ├── 📂 model_trainer/       # Trained models
│   └── 📂 model_evaluation/    # Performance metrics
├── 📂 k8s/                     # Kubernetes manifests
│   ├── deployment.yaml         # Application deployment
│   ├── service.yaml           # Service configuration
│   └── ingress.yaml           # Ingress routing
├── 📂 observability/           # Monitoring stack
│   ├── docker-compose.yml     # Complete monitoring setup
│   ├── 📂 prometheus/         # Metrics collection
│   ├── 📂 grafana/           # Visualization dashboards
│   ├── 📂 elasticsearch/     # Log storage
│   └── 📂 kibana/            # Log analysis
├── 📂 .github/workflows/       # CI/CD automation
│   └── ci-cd.yml              # Complete MLOps pipeline
├── dvc.yaml                   # DVC pipeline definition
├── Dockerfile                 # Container definition
├── model_dag.py              # Airflow DAG definition
└── app.py                    # Flask application
```

---

## �📈 Model Performance

**Current model performance metrics:**

- **Algorithm**: XGBoost Classifier
- **Accuracy**: 92.15%
- **Precision**: 91.47%
- **Recall**: 92.00%  
- **F1-Score**: 91.64%
- **AUC**: 94.04%

Performance tracking via MLflow with experiment comparison and model registry integration.

---


### **Infrastructure Components**
- **Container Orchestration**: Kubernetes with auto-scaling
- **Service Mesh**: Istio for traffic management (optional)
- **Data Storage**: DVC for version control, MLflow for experiments
- **Monitoring**: Full observability stack with metrics, logs, traces
- **CI/CD**: Automated testing, security scanning, deployment

---

## 🎯 Conclusion

This MLOps pipeline demonstrates **Development and Devployment-ready machine learning operations** with:

✅ **End-to-End Automation**: From data ingestion to model deployment  
✅ **Scalable Infrastructure**: Kubernetes orchestration with monitoring  
✅ **Quality Assurance**: Automated testing, validation, and security scanning  
✅ **Observability**: Comprehensive metrics, logging, and tracing  
✅ **Continuous Integration**: GitHub Actions for automated workflows  
✅ **Model Governance**: Version control, experiment tracking, performance monitoring  

The pipeline achieves **92.15% model accuracy** while maintaining production standards for reliability, scalability, and maintainability. It serves as a blueprint for implementing MLOps best practices in enterprise environments.

### **Key Achievements:**
- 🔄 Fully automated 6-stage ML pipeline
- 🐳 Containerized deployment with security best practices
- ☸️ Kubernetes orchestration with service mesh capabilities
- 📊 Real-time monitoring and alerting system
- 🚀 CI/CD automation with quality gates
- 📈 Model performance tracking and drift detection

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

</div>

---

## 📋 **Complete Observability Documentation**

**For detailed setup instructions and usage of the complete observability stack, see [Observability.md](Observability.md)**

### **Production Features:**
- **Single Application**: `production_app.py` with integrated monitoring
- **15+ ML Metrics**: Real-time model performance tracking
- **Structured Logging**: Request tracing with Elasticsearch
- **Health Monitoring**: Comprehensive system status endpoints
- **Monitoring Stack**: Prometheus + Grafana + Elasticsearch + Kibana

### **Quick Start:**
```bash
# Start production app with observability
python production_app.py

# Start monitoring stack
cd observability && docker compose up -d

# Access monitoring tools
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# Kibana: http://localhost:5601
```
