# Observability Guide for ML Pipeline

This guide explains how to set up, run, and monitor the observability stack for your ML pipeline, both manually and using a shell script.

---

## 🚀 Overview

The observability stack includes:
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **Jaeger**: Distributed tracing
- **ELK Stack (Elasticsearch, Kibana, Fluentd)**: Centralized logging

All configuration files are in the `observability/` directory.

---

## 1️⃣ Manual Setup

### 1.1. Start the Observability Stack (Docker Compose)

Open a terminal and run:
```powershell
cd observability
# Start all services in the background
docker-compose up -d
```

### 1.2. Access Dashboards
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (default login: admin / admin)
- **Jaeger**: http://localhost:16686
- **Kibana**: http://localhost:5601

### 1.3. Stop the Observability Stack
```powershell
cd observability
docker-compose down
```

---

## 2️⃣ Using a Shell Script

A shell script can automate starting and stopping the observability stack. Create a file named `run_observability.ps1` in the project root with the following content:

```powershell
# run_observability.ps1
param(
    [string]$action = "up"
)

cd observability
if ($action -eq "up") {
    docker-compose up -d
    Write-Host "Observability stack started."
    Write-Host "Prometheus: http://localhost:9090"
    Write-Host "Grafana: http://localhost:3000"
    Write-Host "Jaeger: http://localhost:16686"
    Write-Host "Kibana: http://localhost:5601"
} elseif ($action -eq "down") {
    docker-compose down
    Write-Host "Observability stack stopped."
} else {
    Write-Host "Usage: .\run_observability.ps1 [up|down]"
}
```

### Usage:
```powershell
# To start all services
.\run_observability.ps1 up

# To stop all services
.\run_observability.ps1 down
```

---

## 3️⃣ Monitoring Your ML Pipeline

- **Metrics**: Exposed at `http://localhost:8000/metrics` (from your ML pipeline)
- **Logs**: Collected and viewable in Kibana
- **Traces**: View request traces in Jaeger
- **Dashboards**: Grafana for real-time metrics and custom dashboards

---

## 4️⃣ Troubleshooting
- Ensure Docker is running
- Ports 9090, 3000, 16686, 5601 are not blocked
- Use `docker-compose logs` in the `observability/` folder to view service logs

---

## 5️⃣ Customization
- Edit `observability/prometheus/prometheus.yml` to add/remove metrics targets
- Add Grafana dashboards in `observability/grafana/provisioning/dashboards/`
- Update Fluentd config in `observability/fluentd/fluent.conf` for log routing

---

**You now have full observability for your ML pipeline!**
