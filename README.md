# CloudOps Hub

CloudOps Hub is a cloud infrastructure and DevOps portfolio project built to demonstrate AWS networking, Infrastructure as Code, Docker containerization, and CI/CD practices.

## Project Goals

- Provision AWS networking resources using Terraform.
- Build and run a web dashboard in Docker.
- Organize infrastructure configuration using reusable variables and outputs.
- Automate validation and Docker image builds with GitHub Actions.
- Extend the dashboard with real AWS monitoring metrics.

## Architecture

The current Terraform infrastructure includes:

- AWS VPC
- Public and private subnets
- Internet Gateway
- Public and private route tables
- Route table associations
- Security groups with explicit security rules

The web dashboard is packaged as an NGINX Docker container.

## Technologies

- AWS
- Terraform
- Docker
- NGINX
- HTML, CSS, and JavaScript
- Git and GitHub
- GitHub Actions

## Run the Dashboard Locally

From the project root:

```bash
docker build -t cloudops-hub:latest ./app
docker run -d --name cloudops-hub -p 8080:80 cloudops-hub:latest
