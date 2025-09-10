# CI/CD Setup for ML Pipeline

This document explains the GitHub Actions CI/CD pipeline implementation for the ML Pipeline project.

## Overview

The CI/CD pipeline consists of three main workflows:

1. **Continuous Integration (CI)** - `ci.yml`
2. **Continuous Deployment (CD)** - `cd.yml`
3. **Model Training & Deployment** - `model-training.yml`

## Workflows

### 1. Continuous Integration (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
- **lint-and-format**: Code quality checks using Black, isort, Flake8, MyPy, Bandit, and Safety
- **test**: Unit tests with coverage reporting
- **data-validation**: Sample data validation using pipeline components

**Artifacts:**
- Security reports (Bandit, Safety)
- Coverage reports (XML, HTML)
- Test results
- Data validation reports

### 2. Continuous Deployment (`cd.yml`)

**Triggers:**
- Successful completion of CI workflow on `main` branch
- Push to `main` branch
- Tags starting with `v*`

**Jobs:**
- **build-and-push**: Build and push Docker images to GitHub Container Registry
- **deploy-staging**: Deploy to staging environment
- **run-integration-tests**: Integration tests against staging
- **deploy-production**: Deploy to production (only on tags)
- **notify**: Slack notifications on success/failure
- **rollback**: Automatic rollback on deployment failure

### 3. Model Training & Deployment (`model-training.yml`)

**Triggers:**
- Weekly schedule (Sundays at 2 AM UTC)
- Manual trigger with options for retraining and data source

**Jobs:**
- **data-ingestion**: Download and validate data
- **feature-engineering**: Engineer features from raw data
- **model-training**: Train and evaluate models
- **deploy-model**: Deploy new model if accuracy > 80%
- **model-monitoring**: Setup monitoring for new model
- **cleanup**: Clean up old artifacts

## Setup Instructions

### 1. Repository Secrets

Add the following secrets to your GitHub repository:

```
KAGGLE_JSON          # Kaggle API credentials
SLACK_WEBHOOK        # Slack webhook URL for notifications
K8S_STAGING_SERVER   # Kubernetes staging server URL
K8S_STAGING_TOKEN    # Kubernetes staging access token
K8S_PROD_SERVER      # Kubernetes production server URL
K8S_PROD_TOKEN       # Kubernetes production access token
```

### 2. Environment Setup

Create the following GitHub environments:
- `staging` - for staging deployments
- `production` - for production deployments (with protection rules)

### 3. Docker Registry

The pipeline uses GitHub Container Registry (ghcr.io). Ensure your repository has:
- Container registry enabled
- Appropriate permissions for pushing images

### 4. Kubernetes Setup

Update the Kubernetes configuration files in `k8s/` directory:
- Replace placeholder values with actual cluster details
- Configure persistent volumes for artifacts
- Set up ingress rules as needed

## Docker Configuration

### Base Dockerfile

The `Dockerfile` includes:
- Multi-stage build for optimization
- Non-root user for security
- Health checks
- Observability tools integration
- Production and observability variants

### Image Variants

- **base**: Standard application image
- **production**: Production-optimized image
- **observability**: Image with additional monitoring tools

## Testing Strategy

### Unit Tests (`tests/unit/`)

- Component-level tests for ML pipeline modules
- Mock external dependencies
- Test configuration and data processing

### Integration Tests (`tests/integration/`)

- End-to-end API testing
- Pipeline integration testing
- Observability stack testing
- Data quality validation

### Test Configuration

Tests use:
- pytest framework
- Coverage reporting
- Fixtures for sample data
- Mock external services

## Code Quality

### Linting and Formatting

- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting
- **Flake8**: Style guide enforcement
- **MyPy**: Static type checking
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency security checking

### Configuration Files

- `.flake8`: Flake8 configuration
- `pyproject.toml`: Black, isort, MyPy, pytest configuration

## Observability Integration

The CI/CD pipeline integrates with the observability stack:

### Metrics
- Prometheus metrics exposed on port 8000
- Pipeline performance metrics
- Deployment success/failure metrics

### Logging
- Structured JSON logging
- ELK stack integration
- Pipeline stage logging

### Tracing
- Jaeger integration for request tracing
- Pipeline execution tracing

## Deployment Strategy

### Rolling Deployments
- Zero-downtime deployments using Kubernetes rolling updates
- Health checks before routing traffic
- Automatic rollback on failure

### Environments
- **Staging**: Automatic deployment from main branch
- **Production**: Manual approval required, triggered by tags

### Monitoring
- Post-deployment health checks
- Performance monitoring
- Alerting on deployment failures

## Model Lifecycle Management

### Automated Training
- Weekly scheduled training
- Data drift detection
- Model performance validation
- Automatic deployment of improved models

### Model Versioning
- Timestamp-based versioning
- Artifact storage with retention policies
- Model performance tracking

### A/B Testing Support
- Infrastructure for model comparison
- Traffic splitting capabilities
- Performance metrics collection

## Troubleshooting

### Common Issues

1. **Failed Tests**: Check test logs in GitHub Actions
2. **Docker Build Failures**: Verify Dockerfile and dependencies
3. **Deployment Failures**: Check Kubernetes cluster status
4. **Model Training Failures**: Verify data availability and quality

### Debugging

- Use GitHub Actions logs for detailed error information
- Check artifact uploads for intermediate results
- Use `workflow_dispatch` for manual testing
- Monitor observability dashboards for runtime issues

## Extending the Pipeline

### Adding New Jobs

1. Create new job in appropriate workflow file
2. Define dependencies using `needs`
3. Add appropriate triggers and conditions
4. Update documentation

### Custom Actions

Consider creating custom GitHub Actions for:
- Model deployment
- Data quality checks
- Notification systems
- Integration with external tools

## Security Considerations

### Best Practices

- Use non-root containers
- Scan for vulnerabilities (Bandit, Safety)
- Secure secret management
- Network policies in Kubernetes
- Regular dependency updates

### Compliance

- Audit trail through GitHub Actions logs
- Artifact retention policies
- Access control through environments
- Security scanning in CI pipeline

## Performance Optimization

### Build Optimization

- Multi-stage Docker builds
- Layer caching
- Parallel job execution
- Artifact caching

### Resource Management

- Appropriate resource limits in Kubernetes
- Auto-scaling configuration
- Cost optimization through scheduling

## Monitoring and Alerting

### Pipeline Monitoring

- GitHub Actions workflow status
- Deployment success rates
- Test failure trends
- Performance metrics

### Integration with Observability

- Prometheus metrics for CI/CD events
- Grafana dashboards for pipeline visualization
- Alerting on failures and performance degradation

---

This CI/CD setup provides a robust, scalable, and observable deployment pipeline for your ML project with comprehensive testing, security scanning, and automated deployments.
