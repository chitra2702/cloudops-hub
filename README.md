# CloudOps Hub

CloudOps Hub is a cloud infrastructure and DevOps portfolio project demonstrating AWS networking, Infrastructure as Code (IaC), Docker containerization, CI automation, and container deployment on EC2.

## Project Goals

- Provision AWS networking resources using Terraform.
- Build and run a web dashboard using Docker and NGINX.
- Organize infrastructure configuration using reusable variables, modules, and outputs.
- Automate Terraform validation and Docker image publishing with GitHub Actions.
- Deploy the published Docker image on an AWS EC2 instance.
- Extend the dashboard with real AWS CloudWatch metrics.
- Automate deployment to AWS through CI/CD.

## Architecture

The project currently includes the following AWS networking resources:

- Virtual Private Cloud (VPC)
- Public and private subnets
- Internet Gateway
- Public and private route tables
- Route table associations
- Security groups with explicit security rules

The dashboard is packaged in an NGINX Docker container and published to Docker Hub.

### CI/CD Workflow

1. Code is maintained in GitHub.
2. GitHub Actions validates Terraform formatting and configuration.
3. GitHub Actions builds the Docker image.
4. The workflow authenticates with Docker Hub using GitHub Actions secrets.
5. The image is published to Docker Hub.
6. The published image can be pulled and run on an EC2 instance.

**Note:** Docker image publishing is automated. AWS deployment automation is a separate planned enhancement.

## Technologies

- AWS VPC and EC2
- Terraform
- Docker
- NGINX
- HTML, CSS, and JavaScript
- Git and GitHub
- GitHub Actions
- Docker Hub
- AWS CloudWatch (planned dashboard integration)

## Repository Structure

```text
secure-aws-terraform/
├── app/
│   ├── Dockerfile
│   └── index.html
├── modules/
├── .github/
│   └── workflows/
│       └── ci.yml
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
├── docker-compose.yml
└── README.md
```

## Run the Dashboard Locally

Run these commands from the project root:

```bash
docker build -t cloudops-hub:latest ./app

docker run -d \
  --name cloudops-hub \
  -p 8080:80 \
  cloudops-hub:latest
```

Open the dashboard at:

`http://localhost:8080`

To check the container:

```bash
docker ps
curl -I http://localhost:8080
```

To stop and remove the container:

```bash
docker stop cloudops-hub
docker rm cloudops-hub
```

## Run the Published Image on EC2

Pull the latest published image:

```bash
docker pull chitramanam/cloudops-hub:latest
```

Run the dashboard:

```bash
docker run -d \
  --name cloudops-hub \
  --restart unless-stopped \
  -p 8080:80 \
  chitramanam/cloudops-hub:latest
```

Verify the deployment on the EC2 instance:

```bash
docker ps
curl -I http://localhost:8080
```

For external browser access, configure the EC2 security group to allow inbound TCP traffic on port 8080 only from the intended source.

- GitHub repository: https://github.com/chitra2702/cloudops-hub
- Docker Hub image: https://hub.docker.com/r/chitramanam/cloudops-hub

## Terraform Workflow

From the directory containing the Terraform configuration:

```bash
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan
```

Review the plan before applying any infrastructure changes.

```bash
terraform apply
```

Terraform state contains information about managed infrastructure. Keep state files and sensitive configuration out of public Git repositories.

## Current Dashboard Status

The dashboard currently displays demonstration metrics. It does not yet retrieve live metrics from CloudWatch.

Planned monitoring enhancements include:

- EC2 CPU utilization
- Network traffic metrics
- Instance status checks
- CloudWatch-backed metric retrieval
- Appropriate access permissions and monitoring configuration

## Future Enhancements

- Integrate real AWS CloudWatch metrics into the dashboard.
- Automate AWS deployment after successful CI checks.
- Add deployment verification and failure handling.
- Improve monitoring and operational documentation.

## Cost Management and Cleanup

Before removing AWS resources:

1. Confirm that the latest source code and documentation are pushed to GitHub.
2. Review the Terraform state and identify all managed resources.
3. If you intend to remove the Terraform-managed infrastructure, review `terraform plan -destroy` and confirm the resources before running `terraform destroy`.
4. Terminate the EC2 instance when it is no longer required.
5. Check for remaining EBS volumes, snapshots, Elastic IP addresses, NAT gateways, load balancers, and other billable resources.
6. Verify the remaining resources in the AWS Console.

Stopping an EC2 instance does not stop charges for its attached EBS storage. Confirm whether volumes are retained before deleting anything.

## Project Status

- Terraform infrastructure and outputs: Completed
- GitHub Actions CI: Completed
- Automatic Docker Hub image publishing: Completed
- Published Docker image on EC2: Previously completed; verify before cleanup
- Final README documentation: In progress
- Real CloudWatch metrics: Planned
- Automated AWS deployment: Planned

