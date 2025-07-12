# Azure Serverless Cost Optimization – Billing Records Archive Solution

---

## Objective

Implement a cost-efficient and scalable solution for managing large volumes of billing records in Azure Cosmos DB by archiving infrequently accessed data—ensuring no data loss, no downtime, and zero changes to existing APIs.

---

## Solution Summary

The existing system uses Azure Cosmos DB to store over 2 million billing records, each up to 300 KB in size. Most reads target recent data, while records older than 3 months are rarely accessed.

To reduce storage and throughput costs in Cosmos DB, this solution introduces a **hot–cold data tiering strategy**:

- **Hot data** (≤ 3 months): Stays in Cosmos DB
- **Cold data** (> 3 months): Archived in Azure Blob Storage (Cool or Archive tier)
- **Azure Functions** handle scheduled archival and transparent read access to both tiers

This allows us to maintain full access to all records with minimal latency and no architectural changes to the calling APIs.

---

## Architecture Overview
The architecture implements a hot-cold storage model where recent billing records (hot data) reside in Cosmos DB for fast access. Older records (cold data) are periodically archived to Azure Blob Storage using an Azure Function triggered by a timer. When a record is requested, a read proxy function first attempts to retrieve it from Cosmos DB, falling back to Blob Storage if not found. This ensures seamless access without API changes while optimizing costs by reducing storage and throughput charges in Cosmos DB.

---

##  Key Azure Components Used

| Azure Service                  | Purpose                                                                 |
|--------------------------------|-------------------------------------------------------------------------|
| **Cosmos DB**                  | Primary store for hot billing records                                   |
| **Azure Blob Storage**         | Archive layer for cold records (> 3 months)                             |
| **Azure Functions**            | - Archive old records<br> - Read-through fallback logic                 |
| **Azure Timer Trigger**        | Runs archival logic daily/weekly                                        |
| **Azure Monitor (Optional)**   | Observability and alerts                                                |
| **Azure Key Vault (Optional)** | Secure secrets for DB and Storage access                                |

---

##  Functional Breakdown

### 1. Archive Function (Timer Trigger)
- Runs on a schedule (e.g., daily)
- Queries Cosmos DB for records older than 90 days
- Stores them as `.json` in Blob Storage (organized by date)
- Deletes archived records from Cosmos DB to reduce cost

### 2. Read Proxy Function
- Receives record ID requests
- First checks Cosmos DB
- If not found, retrieves from Blob Storage
- Optionally caches cold records back to Cosmos DB (read-through)

### 3. Write Function
- Remains unchanged — all new records go directly into Cosmos DB

---

## Why This Works

| Criteria                         | Achieved? | Explanation                                               |
|----------------------------------|-----------|-----------------------------------------------------------|
| **Cost Optimization**            | ✅        | Blob storage is ~10x cheaper than Cosmos DB for cold data |
| **No Downtime**                  | ✅        | All transitions are done asynchronously                   |
| **No Data Loss**                 | ✅        | Archival preserves full records in Blob                   |
| **No API Contract Changes**      | ✅        | Read/write operations remain unchanged externally         |
| **Simple to Maintain**           | ✅        | Uses native Azure Functions and storage lifecycle rules   |

---

## Security & Access
- Use Azure Key Vault or Managed Identities for secure access to Cosmos DB and Blob

- Blob access can be limited using RBAC and Private Endpoints

- Optionally enable encryption, access logging, and retention policies

---

## Cost Impact Summary

|Resource	               |Before	                  |After (Estimated)          |
|------------------------|--------------------------|---------------------------|
|Cosmos DB Storage	     |Full 2M records	          |Hot data only (~3 months)  |
|Cosmos RU Consumption	 |Higher due to cold reads	|Lower due to hot-only      |
|Blob Storage (Cool)	   |Not used	                |~₹1–2/GB/month (cheap)     |
|Azure Functions	       |Not used	                |Pay-per-execution (minimal)|

---

## Conclusion
This solution delivers significant cost savings by leveraging native Azure services in a hot–cold storage design. It:

- Requires no downtime or API changes

- Maintains performance and availability

- Is easy to deploy and maintain

- The architecture is scalable, secure, and ready for production use.

---

## Optional: Terraform Setup for Infrastructure Provisioning

To automate provisioning, an optional terraform setup is included under `infra/terraform/`.

### What It Deploys

- Azure Resource Group  
- Azure Cosmos DB Account  
- Azure Blob Storage  
- Azure Function App (consumption plan)  
- App Settings for environment variables

bash
Copy
Edit

### How to Use

1. Navigate to the terraform directory:
   ```bash
   cd infra/terraform
Initialize and apply:

bash
Copy
Edit
terraform init
terraform apply
After creation, manually upload your Function code or automate deployment via GitHub Actions.
