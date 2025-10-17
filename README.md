<div align="center">

# MACHINE LEARNING OPERATIONS PIPELINE

![last commit](https://img.shields.io/github/last-commit/Abeshith/MLOps_PipeLine?color=blue&label=last%20commit&style=flat)
![Python](https://img.shields.io/badge/python-84.2%25-blue&style=flat)
![Languages](https://img.shields.io/badge/languages-4-lightgrey&style=flat)

## Built with the tools and technologies:

![Flask](https://img.shields.io/badge/Flask-black?style=flat&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-orange?style=flat&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-orange?style=flat&logo=xgboost&logoColor=white)
![DVC](https://img.shields.io/badge/DVC-blue?style=flat&logo=dvc&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-blue?style=flat&logo=mlflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-blue?style=flat&logo=kubernetes&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-blue?style=flat&logo=apache-airflow&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-blue?style=flat&logo=github-actions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-orange?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-orange?style=flat&logo=grafana&logoColor=white)

</div>

---

## 📊 **About the Project**

This repository demonstrates a **comprehensive MLOps pipeline** that showcases industry-standard practices for end-to-end machine learning workflow automation. The project implements a production-ready ML system with automated training, validation, deployment, and monitoring capabilities.

### 🎯 **Key Features**

- **6-Stage DVC Pipeline**: Data ingestion → Validation → Feature engineering → Transformation → Training → Evaluation
- **XGBoost Model**: Achieved 92.15% accuracy with automated hyperparameter tuning
- **MLflow Integration**: Experiment tracking and model registry for version control
- **Production Monitoring**: 15+ ML metrics with Prometheus, Grafana dashboards, and health endpoints
- **Container Orchestration**: Docker containerization with Kubernetes deployment
- **CI/CD Automation**: GitHub Actions for testing, security scanning, and deployment

---

## 🚀 **Getting Started**

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
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## 🔄 **Pipeline Execution**

### Complete Pipeline
```bash
# Run all stages
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python main.py

# Or use DVC
dvc repro
```

### Individual Stages
```bash
# Stage 1: Data Ingestion
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python -m src.mlpipeline.pipeline.stage_01_data_ingestion

# Stage 2: Data Validation  
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python -m src.mlpipeline.pipeline.stage_02_data_validation

# Stage 3: Feature Engineering
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python -m src.mlpipeline.pipeline.stage_03_feature_engineering

# Stage 4: Data Transformation
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python -m src.mlpipeline.pipeline.stage_04_data_transformation

# Stage 5: Model Training
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python -m src.mlpipeline.pipeline.stage_05_model_trainer

# Stage 6: Model Evaluation
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python -m src.mlpipeline.pipeline.stage_06_model_evaluation
```

### Flask Application
```bash
# Start web interface
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python app.py
# Access at: http://localhost:5000

# Production app with monitoring
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python production_app.py
# Metrics at: http://localhost:5000/metrics
```

---

## 📊 **Monitoring & Observability**

### Start Monitoring Stack
```bash
cd observability
docker compose up -d

# Access monitoring tools:
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# Kibana: http://localhost:5601
```

### Available Metrics
- **Model Performance**: accuracy, precision, recall, F1-score
- **Prediction Analytics**: confidence scores, class distribution
- **System Health**: error rates, response times, resource usage

📖 **For detailed observability setup and configuration, see [Observability.md](./Observability.md)**

---

## ☸️ **Kubernetes Deployment**

```bash
# Start cluster
minikube start

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Access application
kubectl port-forward svc/mlapp-service 8000:80
# Navigate to: http://localhost:8000
```

---

## 🔧 **Apache Airflow Pipeline**

```bash
# Set up Airflow (Linux/WSL)
export AIRFLOW_HOME=~/airflow
cp model_dag.py ~/airflow/dags/

# Start Airflow
airflow standalone

# Test DAG file
python ~/airflow/dags/model_dag.py

# Access UI: http://localhost:8080
# Trigger: ml_pipeline_dag
```

---

## 📈 **Model Performance**

- **Algorithm**: XGBoost Classifier
- **Accuracy**: 92.15%
- **Precision**: 91.47%
- **Recall**: 92.00%
- **F1-Score**: 91.64%
- **AUC**: 94.04%

---

## 📁 **Project Structure**

```
MLOps_PipeLine/
├── src/mlpipeline/           # Core ML pipeline components and stages
├── config/                   # Configuration files for pipeline settings
├── artifacts/               # Generated model artifacts and data (DVC tracked)
├── k8s/                     # Kubernetes deployment manifests
├── observability/           # Complete monitoring stack with Prometheus, Grafana
├── .github/workflows/       # CI/CD automation pipelines
├── dvc.yaml                # DVC pipeline definition and stages
├── Dockerfile              # Container definition for deployment
├── model_dag.py           # Apache Airflow DAG for pipeline orchestration
├── app.py                 # Basic Flask web application
├── production_app.py      # Production Flask app with monitoring
└── main.py                # Main pipeline execution script
```

---

## 🎯 **Key Achievements**

✅ **End-to-End Automation**: From data ingestion to model deployment  
✅ **Scalable Infrastructure**: Kubernetes orchestration with monitoring  
✅ **Quality Assurance**: Automated testing, validation, and security scanning  
✅ **Observability**: Comprehensive metrics, logging, and tracing  
✅ **Continuous Integration**: GitHub Actions for automated workflows  
✅ **Model Governance**: Version control, experiment tracking, performance monitoring

---

<div align="center">

**⭐ Star this repository if you found it helpful!**
