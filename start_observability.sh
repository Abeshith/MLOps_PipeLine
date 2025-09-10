#!/bin/bash

# ML Pipeline Observability Stack Startup Script

echo "🚀 Starting ML Pipeline Observability Stack..."

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p observability/prometheus/data
mkdir -p observability/grafana/data
mkdir -p observability/elasticsearch/data
mkdir -p observability/fluentd/buffer

# Set permissions
echo "🔒 Setting permissions..."
chmod 755 logs
chmod 755 observability/prometheus/data
chmod 755 observability/grafana/data
chmod 755 observability/elasticsearch/data

# Start the observability stack
echo "🐳 Starting Docker containers..."
cd observability

# Start core infrastructure
echo "Starting Prometheus, Grafana, and supporting services..."
docker-compose up -d prometheus grafana node-exporter

# Wait for Prometheus to be ready
echo "⏳ Waiting for Prometheus to start..."
sleep 10

# Start logging infrastructure
echo "Starting Elasticsearch, Kibana, and Fluentd..."
docker-compose up -d elasticsearch
sleep 30  # Wait for Elasticsearch to be ready
docker-compose up -d kibana fluentd

# Start tracing
echo "Starting Jaeger for distributed tracing..."
docker-compose up -d jaeger

# Start alerting
echo "Starting AlertManager..."
docker-compose up -d alertmanager

echo "✅ All services started!"
echo ""
echo "🌐 Access URLs:"
echo "   Grafana Dashboard:  http://localhost:3000 (admin/mlops123)"
echo "   Prometheus:         http://localhost:9090"
echo "   Jaeger Tracing:     http://localhost:16686"
echo "   Kibana Logs:        http://localhost:5601"
echo "   AlertManager:       http://localhost:9093"
echo ""
echo "📊 To check service status:"
echo "   docker-compose ps"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs [service-name]"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"

# Return to main directory
cd ..

echo "🎯 Starting ML Pipeline application with metrics..."
python app.py
