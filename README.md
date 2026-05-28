KB Assistant — Azure
An AI-powered knowledge base assistant built on Azure. Ask questions in plain English, get answers backed by your own documents. Fully automated infrastructure and deployment pipeline — no manual portal clicks, no local setup required for users.
Live demo: Drop your own docs in /docs, deploy with one command, get a hosted AI assistant for your knowledge base in minutes.

What It Does
You hit a URL, type a question, and the app searches your uploaded documents and returns a natural language answer powered by Azure OpenAI GPT-4o-mini. Password protected. Centrally hosted. Anyone on your team can use it from a browser with no setup.

Architecture
Developer
    │
    │  git push to master
    ▼
GitHub Repository
    │
    ├── infra.yml ──────────────────────────────────────────────────┐
    │   (triggers on /terraform changes)                            │
    │   terraform fmt → validate → plan → apply                    │
    │                                                               ▼
    └── deploy.yml ─────────────────────────────────────────────▶ Azure
        (triggers on /app changes)                                  │
        docker build → push to ACR → update Container App          │
                                                                    │
Azure Resources (all provisioned by Terraform)                      │
    ├── Resource Group                                              │
    ├── Azure Container App  ◀── runs the KB Assistant ────────────┘
    │       │  (Managed Identity — no passwords)
    │       ├──▶ Key Vault       (reads AZURE_OPENAI_KEY at runtime)
    │       ├──▶ Azure OpenAI    (GPT-4o-mini, answers questions)
    │       └──▶ Blob Storage    (reads uploaded /docs)
    ├── Azure Container Registry (stores Docker images)
    ├── Container Apps Environment
    ├── Log Analytics Workspace
    └── Blob Storage  (also stores Terraform remote state)

Tech Stack
LayerTechnologyInfrastructureTerraform (modular)CI/CDGitHub ActionsComputeAzure Container AppsAIAzure OpenAI GPT-4o-miniSecret ManagementAzure Key Vault + Managed IdentityStorageAzure Blob StorageContainer RegistryAzure Container RegistryApp FrameworkPython / FastAPIContainerizationDocker

Why This Architecture
Terraform modules — infrastructure is split into reusable modules (container_app, keyvault, openai, storage). Not one giant main.tf. Each module owns its resources and exposes outputs. Shows how real teams structure IaC.
Remote state — Terraform state lives in Azure Blob Storage, not on a local machine. Shared, locked during runs, recoverable.
Managed Identity — the Container App authenticates to Key Vault without a password. No secrets to rotate, leak, or store. The Azure Identity SDK handles token exchange internally at runtime.
GitHub Actions as the deploy mechanism — terraform apply never runs from a local machine in this setup. The pipeline is the source of truth. Every infrastructure change is auditable via git history.
Container Apps — scales to zero when idle. Zero cost when not in use. No OS patching, no VM management.

Project Structure
kb-assistant-azure/
├── .github/
│   └── workflows/
│       ├── infra.yml          # terraform pipeline
│       └── deploy.yml         # app deploy pipeline
├── terraform/
│   ├── main.tf                # root — calls modules + remote state backend
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── modules/
│       ├── container_app/     # Container App, ACR, Log Analytics
│       ├── keyvault/          # Key Vault, access policies, secrets
│       ├── openai/            # Azure OpenAI cognitive account
│       └── storage/           # Storage account + docs container
├── app/
│   ├── main.py                # FastAPI app
│   ├── ingest.py              # doc loading and chunking
│   ├── retrieval.py           # scoring chunks against queries
│   ├── openai_client.py       # Azure OpenAI integration
│   ├── config.py              # Key Vault secret retrieval
│   ├── requirements.txt
│   └── Dockerfile
├── docs/                      # drop your .md or .txt files here
└── README.md

Cost
ServiceRunningTorn DownAzure Container Apps~$0 (scales to zero)$0Azure OpenAI GPT-4o-miniFractions of a cent per query$0Blob Storage~$0.50–1/mo$0Key Vault~$0.03/10k operations$0GitHub ActionsFree (public repo)$0Total~$1–3/month$0
Run terraform destroy when not in use. Spin it back up in under 2 minutes when you need it.

Prerequisites

Azure subscription
Azure OpenAI access approved (request here)
Terraform CLI installed
Docker installed
Azure CLI installed


Deploy Your Own
1. Bootstrap Terraform state storage (one time only)
bashaz login
az group create --name rg-terraform-state --location eastus
az storage account create --name <unique-name> --resource-group rg-terraform-state --location eastus --sku Standard_LRS
az storage container create --name tfstate --account-name <unique-name>
2. Create a Service Principal for GitHub Actions
bashaz ad sp create-for-rbac --name "sp-kb-assistant-github" --role Contributor \
  --scopes /subscriptions/<your-subscription-id> --sdk-auth
Save the JSON output as a GitHub Secret named AZURE_CREDENTIALS.
3. Set GitHub Secrets
SecretValueAZURE_CREDENTIALSJSON from Service PrincipalOPENAI_API_KEYYour Azure OpenAI API keyAPP_PASSWORDPassword to access the app UIACR_USERNAMEYour ACR nameACR_PASSWORDYour ACR admin password
4. Configure Terraform variables
bashcp terraform/terraform.tfvars.example terraform/terraform.tfvars
# fill in your values
5. Deploy
bashcd terraform
terraform init
terraform apply
After apply completes your infrastructure is live. Push any change to /terraform and the pipeline handles future updates. Push any change to /app and the pipeline builds and deploys the new Docker image automatically.
6. Add your docs
Upload .md or .txt files to the docs container in your Blob Storage account. Restart the Container App revision to reload.

How to Use

Hit your Container App URL
Enter your APP_PASSWORD
Ask a question about your documents
Get an AI-generated answer with sources cited


Tear Down
bashcd terraform
terraform destroy
All resources deleted in under 2 minutes. State remains in your Blob Storage backend so you can redeploy cleanly anytime.

Background
V1 of this tool was built at a previous role to solve a real support problem — agents couldn't find answers fast enough across a large knowledge base. It worked but had limitations: everyone ran it locally with their own API key, no central deployment, company owned the code.
V2 is the rebuild done right. Proper Azure infrastructure provisioned with Terraform, automated deployment via GitHub Actions, Azure OpenAI for the AI layer, Key Vault for secret management, containerized with Docker. Architected as a reusable template so any team can deploy it with their own knowledge base.