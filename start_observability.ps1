# ML Pipeline Observability Stack Startup Script for Windows

Write-Host "🚀 Starting ML Pipeline Observability Stack..." -ForegroundColor Green

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs"
New-Item -ItemType Directory -Force -Path "observability\prometheus\data"
New-Item -ItemType Directory -Force -Path "observability\grafana\data"
New-Item -ItemType Directory -Force -Path "observability\elasticsearch\data"
New-Item -ItemType Directory -Force -Path "observability\fluentd\buffer"

# Navigate to observability directory
Set-Location "observability"

# Start core infrastructure
Write-Host "🐳 Starting Docker containers..." -ForegroundColor Yellow
Write-Host "Starting Prometheus, Grafana, and supporting services..." -ForegroundColor Blue
docker-compose up -d prometheus grafana node-exporter

# Wait for Prometheus to be ready
Write-Host "⏳ Waiting for Prometheus to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Start logging infrastructure
Write-Host "Starting Elasticsearch, Kibana, and Fluentd..." -ForegroundColor Blue
docker-compose up -d elasticsearch
Start-Sleep -Seconds 30  # Wait for Elasticsearch to be ready
docker-compose up -d kibana fluentd

# Start tracing
Write-Host "Starting Jaeger for distributed tracing..." -ForegroundColor Blue
docker-compose up -d jaeger

# Start alerting
Write-Host "Starting AlertManager..." -ForegroundColor Blue
docker-compose up -d alertmanager

Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access URLs:" -ForegroundColor Cyan
Write-Host "   Grafana Dashboard:  http://localhost:3000 (admin/mlops123)" -ForegroundColor White
Write-Host "   Prometheus:         http://localhost:9090" -ForegroundColor White
Write-Host "   Jaeger Tracing:     http://localhost:16686" -ForegroundColor White
Write-Host "   Kibana Logs:        http://localhost:5601" -ForegroundColor White
Write-Host "   AlertManager:       http://localhost:9093" -ForegroundColor White
Write-Host ""
Write-Host "📊 To check service status:" -ForegroundColor Cyan
Write-Host "   docker-compose ps" -ForegroundColor White
Write-Host ""
Write-Host "📋 To view logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs [service-name]" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop all services:" -ForegroundColor Cyan
Write-Host "   docker-compose down" -ForegroundColor White

# Return to main directory
Set-Location ".."

Write-Host "🎯 Ready to start ML Pipeline application with metrics!" -ForegroundColor Green
Write-Host "Run: python app.py" -ForegroundColor Yellow
