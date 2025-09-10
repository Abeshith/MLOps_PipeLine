# MLOps Pipeline Local Development Script

Write-Host "🚀 MLOps Pipeline Local Development Setup" -ForegroundColor Green

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        docker info | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to build and run the application
function Start-MLOpsPipeline {
    param(
        [switch]$Build,
        [switch]$Compose
    )
    
    if (-not (Test-DockerRunning)) {
        Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
        exit 1
    }
    
    if ($Build) {
        Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
        docker build -t mlops-pipeline:latest .
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Docker build failed!" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    }
    
    if ($Compose) {
        Write-Host "🐳 Starting services with Docker Compose..." -ForegroundColor Yellow
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Services started successfully!" -ForegroundColor Green
            Write-Host "📱 Application: http://localhost:5000" -ForegroundColor Cyan
            Write-Host "📊 Prometheus: http://localhost:9090" -ForegroundColor Cyan
            Write-Host "📈 Grafana: http://localhost:3000 (admin/admin)" -ForegroundColor Cyan
        } else {
            Write-Host "❌ Failed to start services!" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "🏃 Running MLOps Pipeline container..." -ForegroundColor Yellow
        docker run --rm -p 5000:5000 -p 8000:8000 -v "${PWD}/artifacts:/app/artifacts" mlops-pipeline:latest
    }
}

# Function to run tests
function Test-MLOpsPipeline {
    Write-Host "🧪 Running pipeline validation tests..." -ForegroundColor Yellow
    python scripts/validate_pipeline.py
}

# Function to stop services
function Stop-MLOpsPipeline {
    Write-Host "🛑 Stopping services..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "✅ Services stopped!" -ForegroundColor Green
}

# Function to clean up Docker resources
function Clear-MLOpsResources {
    Write-Host "🧹 Cleaning up Docker resources..." -ForegroundColor Yellow
    docker-compose down -v --remove-orphans
    docker system prune -f
    Write-Host "✅ Cleanup completed!" -ForegroundColor Green
}

# Main menu
function Show-Menu {
    Write-Host "`n=== MLOps Pipeline Development Menu ===" -ForegroundColor Cyan
    Write-Host "1. Build Docker image"
    Write-Host "2. Run single container"
    Write-Host "3. Start all services (Docker Compose)"
    Write-Host "4. Run validation tests"
    Write-Host "5. Stop all services"
    Write-Host "6. Clean up resources"
    Write-Host "7. Exit"
    Write-Host "========================================"
}

# Main script
if ($args.Count -gt 0) {
    switch ($args[0]) {
        "build" { Start-MLOpsPipeline -Build }
        "run" { Start-MLOpsPipeline -Build; Start-MLOpsPipeline }
        "compose" { Start-MLOpsPipeline -Compose }
        "test" { Test-MLOpsPipeline }
        "stop" { Stop-MLOpsPipeline }
        "clean" { Clear-MLOpsResources }
        default { 
            Write-Host "Usage: .\dev.ps1 [build|run|compose|test|stop|clean]" -ForegroundColor Yellow
            Show-Menu
        }
    }
} else {
    do {
        Show-Menu
        $choice = Read-Host "Please select an option (1-7)"
        
        switch ($choice) {
            "1" { Start-MLOpsPipeline -Build }
            "2" { Start-MLOpsPipeline -Build; Start-MLOpsPipeline }
            "3" { Start-MLOpsPipeline -Compose }
            "4" { Test-MLOpsPipeline }
            "5" { Stop-MLOpsPipeline }
            "6" { Clear-MLOpsResources }
            "7" { 
                Write-Host "👋 Goodbye!" -ForegroundColor Green
                break 
            }
            default { Write-Host "Invalid option. Please try again." -ForegroundColor Red }
        }
        
        if ($choice -ne "7") {
            Read-Host "`nPress Enter to continue..."
        }
    } while ($choice -ne "7")
}
