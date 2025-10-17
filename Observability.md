# ML Pipeline Observability Stack - Complete Guide

## 🎯 **Overview**

This guide provides step-by-step instructions for implementing and using the complete observability stack for the ML Pipeline. The stack includes Prometheus (metrics), Grafana (dashboards), Elasticsearch (logs), and Kibana (log analysis).

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │───▶│   Prometheus    │───▶│    Grafana      │
│ production_app  │    │  (Metrics)      │    │ (Dashboards)    │
│                 │    │ localhost:9090  │    │ localhost:3000  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│ Elasticsearch   │───▶│     Kibana      │
│   (Logs)        │    │ (Log Analysis)  │
│ localhost:9200  │    │ localhost:5601  │
└─────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### **Step 1: Start the Production Application**
```bash
cd "/home/abhes/MlOps PipeLine" && source venv/bin/activate && PYTHONPATH="/home/abhes/MlOps PipeLine/src" python production_app.py
```

### **Step 2: Start Observability Stack**
```bash
cd observability
docker compose up -d
```

### **Step 3: Generate Test Data**
```bash
# Generate predictions to create metrics and logs
for i in {1..20}; do
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{
  "age": '$((25 + RANDOM % 40))',
  "job": "management",
  "marital": "single", 
  "education": "secondary",
  "housing": "yes",
  "loan": "no",
  "duration": '$((100 + RANDOM % 300))',
  "campaign": '$((1 + RANDOM % 5))'
}'
sleep 2
done
```

---

## 📊 **Prometheus Setup & Usage**

### **Access Prometheus**
- **URL**: `http://localhost:9090`
- **Purpose**: Metrics collection and querying

### **Available ML Metrics**
```promql
# Model Performance Metrics
ml_model_accuracy              # Current model accuracy (0.9215)
ml_model_precision            # Model precision
ml_model_recall               # Model recall
ml_model_f1_score            # F1 score

# Prediction Analytics
ml_predictions_total          # Total predictions made
ml_predictions_by_class_total # Predictions by class (0/1)
ml_prediction_confidence      # Prediction confidence distribution
ml_prediction_error_rate      # Current error rate

# System Performance
http_request_duration_seconds # Request latency
ml_feature_processing_seconds # Feature processing time
ml_model_load_seconds        # Model loading time
ml_app_memory_bytes          # Memory usage

# Business Metrics
ml_input_validation_failures_total # Input validation errors
ml_active_users              # Active users count
```

### **Key Prometheus Queries**

**Model Performance:**
```promql
# Model accuracy
ml_model_accuracy

# Prediction rate per minute
rate(ml_predictions_total[1m]) * 60

# Error rate percentage
ml_prediction_error_rate * 100
```

**System Health:**
```promql
# Average request duration
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# 95th percentile latency
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# Memory usage in MB
ml_app_memory_bytes / 1024 / 1024
```

**Business Analytics:**
```promql
# Prediction distribution
ml_predictions_by_class_total

# Average confidence
rate(ml_prediction_confidence_sum[5m]) / rate(ml_prediction_confidence_count[5m])

# Requests per second
rate(ml_predictions_total[1m])
```

### **Prometheus Operations**
```bash
# Check Prometheus health
curl http://localhost:9090/-/healthy

# Query specific metric
curl "http://localhost:9090/api/v1/query?query=ml_model_accuracy"

# Check targets status
curl http://localhost:9090/api/v1/targets

# View configuration
curl http://localhost:9090/api/v1/status/config
```

---

## 📈 **Grafana Dashboard Setup**

### **Access Grafana**
- **URL**: `http://localhost:3000`
- **Login**: `admin/admin` (change on first login)

### **Step 1: Configure Data Source**
1. **Connections** → **Data Sources** → **Add data source**
2. Select **Prometheus**
3. **URL**: `http://prometheus:9090`
4. **Save & Test** (should show green checkmark)

### **Step 2: Create ML Pipeline Dashboard**

#### **Panel 1: Model Performance Overview**
```
Panel Type: Stat
Query: ml_model_accuracy
Title: Model Accuracy
Unit: Percent (0-1)
Thresholds: 
  - Red: < 0.85
  - Yellow: 0.85-0.90
  - Green: > 0.90
```

#### **Panel 2: Prediction Rate**
```
Panel Type: Time series
Query: rate(ml_predictions_total[1m]) * 60
Title: Predictions per Minute
Unit: reqps
Y-axis: Min 0
```

#### **Panel 3: Error Rate**
```
Panel Type: Stat
Query: ml_prediction_error_rate * 100
Title: Error Rate
Unit: Percent
Thresholds:
  - Green: < 5%
  - Yellow: 5-10%
  - Red: > 10%
```

#### **Panel 4: Request Latency**
```
Panel Type: Time series
Query: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
Title: 95th Percentile Latency
Unit: Seconds
```

#### **Panel 5: Prediction Distribution**
```
Panel Type: Pie chart
Query A: ml_predictions_by_class_total{prediction_class="0"}
Query B: ml_predictions_by_class_total{prediction_class="1"}
Title: Prediction Distribution
Legend: No Subscribe / Subscribe
```

#### **Panel 6: System Resources**
```
Panel Type: Time series
Query: ml_app_memory_bytes / 1024 / 1024
Title: Memory Usage
Unit: MB
```

### **Step 3: Dashboard Settings**
- **Time Range**: Last 1 hour
- **Refresh**: 30s
- **Auto-refresh**: Enabled
- **Save Dashboard**: "ML Pipeline Production"

### **Step 4: Create Alerts**
1. **Panel** → **Alert** → **Create Alert Rule**
2. **Model Accuracy Alert**:
   - Condition: `ml_model_accuracy < 0.90`
   - Evaluation: Every 1m for 5m
3. **High Error Rate Alert**:
   - Condition: `ml_prediction_error_rate > 0.10`
   - Evaluation: Every 1m for 2m

---

## 🔍 **Elasticsearch & Kibana Setup**

### **Access Kibana**
- **URL**: `http://localhost:5601`
- **Purpose**: Log analysis and visualization

### **Step 1: Create Data View**
1. **Management** → **Kibana** → **Data Views**
2. **Create data view**
3. **Name**: `ML Pipeline Logs`
4. **Index pattern**: `ml-pipeline-*`
5. **Timestamp field**: `@timestamp`
6. **Save data view**

### **Step 2: Explore Logs**
1. **Analytics** → **Discover**
2. Select **ML Pipeline Logs** data view
3. **Time range**: Last 1 hour

### **Available Log Fields**
```
@timestamp          # Log timestamp
level              # Log level (INFO, ERROR, WARNING)
service            # Service name (ml-pipeline)
message            # Log message
request_id         # Unique request identifier
prediction         # Prediction result (0/1)
confidence         # Prediction confidence
duration           # Request duration
error              # Error details (if any)
model_type         # Model type used
endpoint           # API endpoint called
```

### **Step 3: Create Log Visualizations**

#### **Visualization 1: Log Levels Over Time**
```
Type: Vertical bar chart
X-axis: Date Histogram (@timestamp)
Y-axis: Count
Split series: Terms (level)
```

#### **Visualization 2: Error Analysis**
```
Type: Data table
Columns: @timestamp, level, message, error, request_id
Filter: level:ERROR
Sort: @timestamp desc
```

#### **Visualization 3: Request Duration Trends**
```
Type: Line chart
X-axis: Date Histogram (@timestamp)
Y-axis: Average (duration)
```

#### **Visualization 4: Prediction Success Rate**
```
Type: Metric
Aggregation: Count
Filter: NOT error:*
```

### **Step 4: Create Kibana Dashboard**
1. **Analytics** → **Dashboard** → **Create dashboard**
2. **Add** all visualizations
3. **Save** as "ML Pipeline Logs Dashboard"

### **Step 5: Set Up Log Alerts**
1. **Stack Management** → **Rules and Connectors** → **Rules**
2. **Create rule** → **Elasticsearch query**
3. **Error Rate Alert**:
   - Index: `ml-pipeline-*`
   - Query: `level:ERROR`
   - Threshold: > 5 errors in 5 minutes

---

## 🔧 **Elasticsearch Operations**

### **Direct Elasticsearch Queries**
```bash
# Check cluster health
curl http://localhost:9200/_cluster/health

# List all indices
curl http://localhost:9200/_cat/indices?v

# Search recent logs
curl -X GET "localhost:9200/ml-pipeline-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1h"
      }
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}],
  "size": 10
}'

# Search for errors
curl -X GET "localhost:9200/ml-pipeline-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "level": "ERROR"
    }
  }
}'

# Get prediction statistics
curl -X GET "localhost:9200/ml-pipeline-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "prediction_distribution": {
      "terms": {
        "field": "prediction"
      }
    },
    "avg_confidence": {
      "avg": {
        "field": "confidence"
      }
    }
  },
  "size": 0
}'
```

---

## 🚨 **Alerting & Monitoring**

### **Health Check Endpoints**
```bash
# Application health
curl http://localhost:5000/health

# Detailed status
curl http://localhost:5000/status

# Prometheus metrics
curl http://localhost:5000/metrics
```

### **Service Health Checks**
```bash
# Prometheus
curl http://localhost:9090/-/healthy

# Grafana
curl http://localhost:3000/api/health

# Elasticsearch
curl http://localhost:9200/_cluster/health

# Kibana
curl http://localhost:5601/api/status
```

### **Alert Rules Configuration**
The system includes pre-configured alerts for:
- Model accuracy degradation (< 90%)
- High error rates (> 10%)
- High request latency (> 1s)
- Service unavailability
- Memory usage spikes

---

## 📋 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Issue: No metrics in Prometheus**
```bash
# Check if Flask app is running
curl http://localhost:5000/health

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Restart Prometheus
docker compose restart prometheus
```

#### **Issue: No logs in Kibana**
```bash
# Check Elasticsearch indices
curl http://localhost:9200/_cat/indices?v

# Generate test logs
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"age": 30, "job": "admin", "marital": "single", "education": "secondary", "housing": "yes", "loan": "no", "duration": 200, "campaign": 2}'

# Check if logs are being created
curl http://localhost:9200/ml-pipeline-*/_search?pretty
```

#### **Issue: Grafana can't connect to Prometheus**
1. Check data source URL: `http://prometheus:9090`
2. Verify Prometheus is running: `docker compose ps`
3. Test connection: **Save & Test** in data source

#### **Issue: High memory usage**
```bash
# Check memory metrics
curl -s http://localhost:5000/metrics | grep ml_app_memory_bytes

# Monitor system resources
docker compose stats
```

---

## 📊 **Performance Monitoring**

### **Key Performance Indicators (KPIs)**
- **Model Accuracy**: > 90%
- **Request Latency**: < 500ms (95th percentile)
- **Error Rate**: < 5%
- **Throughput**: > 10 requests/minute
- **Availability**: > 99.9%

### **Monitoring Checklist**
- [ ] All services running (Flask, Prometheus, Grafana, Elasticsearch, Kibana)
- [ ] Metrics being collected (check `/metrics` endpoint)
- [ ] Logs being generated (check Kibana)
- [ ] Dashboards updating (check Grafana)
- [ ] Alerts configured and working
- [ ] Health checks passing

---

## 🔄 **Maintenance & Operations**

### **Daily Operations**
```bash
# Check system health
curl http://localhost:5000/health

# View recent errors
curl -X GET "localhost:9200/ml-pipeline-*/_search?q=level:ERROR&sort=@timestamp:desc&size=5"

# Monitor prediction volume
curl -s http://localhost:9090/api/v1/query?query=rate\(ml_predictions_total\[1h\]\) | jq '.data.result[0].value[1]'
```

### **Weekly Maintenance**
- Review error logs and patterns
- Check model performance trends
- Update alert thresholds if needed
- Clean up old log indices
- Review dashboard effectiveness

### **Backup & Recovery**
```bash
# Backup Grafana dashboards
curl -H "Authorization: Bearer <api-key>" http://localhost:3000/api/search?type=dash-db

# Backup Elasticsearch indices
curl -X PUT "localhost:9200/_snapshot/backup/snapshot_$(date +%Y%m%d)"

# Export Prometheus data
curl http://localhost:9090/api/v1/admin/tsdb/snapshot -XPOST
```

---

## 🎯 **Best Practices**

### **Monitoring Best Practices**
1. **Set appropriate alert thresholds** based on historical data
2. **Use structured logging** for better searchability
3. **Monitor business metrics** alongside technical metrics
4. **Implement gradual alerting** (warning → critical)
5. **Regular dashboard reviews** and updates

### **Performance Optimization**
1. **Optimize query performance** in Prometheus and Elasticsearch
2. **Set appropriate retention policies** for logs and metrics
3. **Use sampling** for high-volume tracing
4. **Monitor resource usage** of observability stack itself

### **Security Considerations**
1. **Secure access** to monitoring dashboards
2. **Sanitize sensitive data** in logs
3. **Use HTTPS** for production deployments
4. **Regular security updates** for all components

---

This comprehensive observability stack provides complete visibility into your ML pipeline's performance, health, and business metrics. Use this guide to implement, maintain, and optimize your monitoring infrastructure.

## 👥 **Contributors**

- **[Abeshith](https://github.com/Abeshith)** - Project Creator & Lead Developer
