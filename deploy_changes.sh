#!/bin/bash

# Add all new files to git
git add tests/
git add .bandit
git add .pre-commit-config.yaml
git add .github/workflows/production-deploy.yml
git add observability/alerts.yml
git add requirements.txt

# Commit changes
git commit -m "Add production-ready CI/CD improvements

- Add comprehensive unit and integration tests
- Add security scanning configuration
- Add pre-commit hooks for code quality
- Add production deployment workflow
- Add monitoring alerts configuration
- Update requirements with testing dependencies"

# Push to main branch
git push origin main

echo "✅ Changes deployed to repository"
