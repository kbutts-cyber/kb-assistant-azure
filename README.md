# KB Assistant — Azure

An AI-powered knowledge base assistant built on Azure. Ask questions in plain English, get answers backed by your own documents. Fully automated infrastructure and deployment pipeline — no manual portal clicks, no local setup required for users.

**Live demo:** Drop your own docs in `/docs`, deploy with one command, get a hosted AI assistant for your knowledge base in minutes.

---

## What It Does

You hit a URL, type a question, and the app searches your uploaded documents and returns a natural language answer powered by Azure OpenAI GPT-4o-mini. Password protected. Centrally hosted. Anyone on your team can use it from a browser with no setup.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Infrastructure | Terraform (modular) |
| CI/CD | GitHub Actions |
| Compute | Azure Container Apps |
| AI | Azure OpenAI GPT-4o-mini |
| Secret Management | Azure Key Vault + Managed Identity |
| Storage | Azure Blob Storage |
| Container Registry | Azure Container Registry |
| App Framework | Python / FastAPI |
| Containerization | Docker |

---

## Why This Architecture

**Terraform modules** — infrastructure split into reusable modules (container_app, keyvault, openai, storage). Not one giant main.tf.

**Remote state** — Terraform state lives in Azure Blob Storage, not on a local machine. Shared, locked during runs, recoverable.

**Managed Identity** — the Container App authenticates to Key Vault without a password. No secrets to rotate, leak, or store.

**GitHub Actions as the deploy mechanism** — `terraform apply` never runs from a local machine. The pipeline is the source of truth. Every change is auditable via git history.

**Container Apps** — scales to zero when idle. Zero cost when not in use. No OS patching, no VM management.

---

## Cost

| Service | Running | Torn Down |
|---|---|---|
| Azure Container Apps | ~$0 (scales to zero) | $0 |
| Azure OpenAI GPT-4o-mini | Fractions of a cent per query | $0 |
| Blob Storage | ~$0.50–1/mo | $0 |
| Key Vault | ~$0.03/10k operations | $0 |
| GitHub Actions | Free (public repo) | $0 |
| **Total** | **~$1–3/month** | **$0** |

---

## Prerequisites

- Azure subscription
- Azure OpenAI access approved
- Terraform CLI installed
- Docker installed
- Azure CLI installed

---

## Deploy Your Own

**1. Bootstrap Terraform state storage (one time only)**

```bash
az login
az group create --name rg-terraform-state --location eastus
az storage account create --name <unique-name> --resource-group rg-terraform-state --location eastus --sku Standard_LRS
az storage container create --name tfstate --account-name <unique-name>
```

**2. Create a Service Principal for GitHub Actions**

```bash
az ad sp create-for-rbac --name "sp-kb-assistant-github" --role Contributor --scopes /subscriptions/<your-subscription-id> --sdk-auth
```

Save the JSON output as a GitHub Secret named `AZURE_CREDENTIALS`.

**3. Set GitHub Secrets**

| Secret | Value |
|---|---|
| `AZURE_CREDENTIALS` | JSON from Service Principal |
| `OPENAI_API_KEY` | Your Azure OpenAI API key |
| `APP_PASSWORD` | Password to access the app UI |
| `ACR_USERNAME` | Your ACR name |
| `ACR_PASSWORD` | Your ACR admin password |

**4. Configure Terraform variables**

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# fill in your values
```

**5. Deploy**

```bash
cd terraform
terraform init
terraform apply
```

**6. Add your docs**

Upload `.md` or `.txt` files to the `docs` container in your Blob Storage account. Restart the Container App revision to reload.

---

## Tear Down

```bash
cd terraform
terraform destroy
```

All resources deleted in under 2 minutes.

---

## Background

V1 of this tool was built at a previous role to solve a real support problem — agents couldn't find answers fast enough across a large knowledge base. Everyone ran it locally with their own API key, no central deployment, company owned the code.

V2 is the rebuild done right. Terraform, GitHub Actions, Azure OpenAI, Key Vault, Docker. Architected as a reusable template so any team can deploy it with their own knowledge base.
