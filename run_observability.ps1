# run_observability.ps1
# PowerShell script to manage the ML Pipeline observability stack

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("up", "down", "restart", "logs", "status")]
    [string]$Action = "up"
)

# Set working directory to observability folder
$observabilityPath = Join-Path $PSScriptRoot "observability"

if (-not (Test-Path $observabilityPath)) {
    Write-Error "Observability directory not found at: $observabilityPath"
    exit 1
}

Set-Location $observabilityPath

Write-Host "🔧 ML Pipeline Observability Stack Manager" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

switch ($Action) {
    "up" {
        Write-Host "🚀 Starting observability stack..." -ForegroundColor Green
        
        # Check if Docker is running
        try {
            docker info | Out-Null
        }
        catch {
            Write-Error "Docker is not running. Please start Docker Desktop and try again."
            exit 1
        }

        # Start all services
        docker-compose up -d

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Observability stack started successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "📊 Access your monitoring tools:" -ForegroundColor Yellow
            Write-Host "   Prometheus:    http://localhost:9090" -ForegroundColor White
            Write-Host "   Grafana:       http://localhost:3000 (admin/admin)" -ForegroundColor White
            Write-Host "   Jaeger:        http://localhost:16686" -ForegroundColor White
            Write-Host "   Kibana:        http://localhost:5601" -ForegroundColor White
            Write-Host "   AlertManager:  http://localhost:9093" -ForegroundColor White
            Write-Host ""
            Write-Host "🔍 Your ML Pipeline metrics endpoint: http://localhost:8000/metrics" -ForegroundColor Cyan
        }
        else {
            Write-Error "Failed to start observability stack. Check docker-compose logs for details."
        }
    }
    
    "down" {
        Write-Host "🛑 Stopping observability stack..." -ForegroundColor Red
        docker-compose down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Observability stack stopped successfully!" -ForegroundColor Green
        }
        else {
            Write-Error "Failed to stop observability stack."
        }
    }
    
    "restart" {
        Write-Host "🔄 Restarting observability stack..." -ForegroundColor Yellow
        docker-compose down
        Start-Sleep -Seconds 3
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Observability stack restarted successfully!" -ForegroundColor Green
            Write-Host ""
            Write-Host "📊 Access your monitoring tools:" -ForegroundColor Yellow
            Write-Host "   Prometheus:    http://localhost:9090" -ForegroundColor White
            Write-Host "   Grafana:       http://localhost:3000 (admin/admin)" -ForegroundColor White
            Write-Host "   Jaeger:        http://localhost:16686" -ForegroundColor White
            Write-Host "   Kibana:        http://localhost:5601" -ForegroundColor White
            Write-Host "   AlertManager:  http://localhost:9093" -ForegroundColor White
        }
    }
    
    "logs" {
        Write-Host "📋 Viewing observability stack logs..." -ForegroundColor Blue
        docker-compose logs -f
    }
    
    "status" {
        Write-Host "📊 Observability stack status:" -ForegroundColor Blue
        Write-Host ""
        docker-compose ps
        
        Write-Host ""
        Write-Host "🔍 Service Health Checks:" -ForegroundColor Yellow
        
        # Check Prometheus
        try {
            $prometheusResponse = Invoke-WebRequest -Uri "http://localhost:9090/-/healthy" -TimeoutSec 5 -UseBasicParsing
            if ($prometheusResponse.StatusCode -eq 200) {
                Write-Host "   Prometheus: ✅ Healthy" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "   Prometheus: ❌ Unhealthy" -ForegroundColor Red
        }
        
        # Check Grafana
        try {
            $grafanaResponse = Invoke-WebRequest -Uri "http://localhost:3000/api/health" -TimeoutSec 5 -UseBasicParsing
            if ($grafanaResponse.StatusCode -eq 200) {
                Write-Host "   Grafana:    ✅ Healthy" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "   Grafana:    ❌ Unhealthy" -ForegroundColor Red
        }
        
        # Check Jaeger
        try {
            $jaegerResponse = Invoke-WebRequest -Uri "http://localhost:16686/" -TimeoutSec 5 -UseBasicParsing
            if ($jaegerResponse.StatusCode -eq 200) {
                Write-Host "   Jaeger:     ✅ Healthy" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "   Jaeger:     ❌ Unhealthy" -ForegroundColor Red
        }
        
        # Check Elasticsearch
        try {
            $elasticResponse = Invoke-WebRequest -Uri "http://localhost:9200/_cluster/health" -TimeoutSec 5 -UseBasicParsing
            if ($elasticResponse.StatusCode -eq 200) {
                Write-Host "   Elasticsearch: ✅ Healthy" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "   Elasticsearch: ❌ Unhealthy" -ForegroundColor Red
        }
        
        # Check Kibana
        try {
            $kibanaResponse = Invoke-WebRequest -Uri "http://localhost:5601/api/status" -TimeoutSec 5 -UseBasicParsing
            if ($kibanaResponse.StatusCode -eq 200) {
                Write-Host "   Kibana:     ✅ Healthy" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "   Kibana:     ❌ Unhealthy" -ForegroundColor Red
        }
    }
    
    default {
        Write-Host "❌ Invalid action: $Action" -ForegroundColor Red
        Write-Host ""
        Write-Host "Usage: .\run_observability.ps1 [up|down|restart|logs|status]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Available actions:" -ForegroundColor Cyan
        Write-Host "  up      - Start the observability stack" -ForegroundColor White
        Write-Host "  down    - Stop the observability stack" -ForegroundColor White
        Write-Host "  restart - Restart the observability stack" -ForegroundColor White
        Write-Host "  logs    - View logs from all services" -ForegroundColor White
        Write-Host "  status  - Check status and health of all services" -ForegroundColor White
    }
}

# Return to original directory
Set-Location $PSScriptRoot
