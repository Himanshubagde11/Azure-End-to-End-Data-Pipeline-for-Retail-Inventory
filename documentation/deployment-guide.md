# CLARIVENS INVENTORY INTELLIGENCE — DEPLOYMENT & OPERATION GUIDE
**Organization:** CLARIVENS RETAIL GROUP  
**Platform:** Azure Retail Inventory Data Pipeline & Analytics Platform  
**Version:** 1.0.0 (Production Architecture)

---

## 1. Overview & Dual Execution Model

To ensure transparency, reliability, and practical testability, this project supports two distinct workflows:

1. **Local Simulation Workflow:** Allows any engineer or interviewer to clone the repository, generate all 178,000+ data records, execute the modular Python Data Quality Framework, populate a local relational Star Schema warehouse, run automated integrity tests, and review pre-rendered Power BI dashboard screenshots without an Azure subscription.
2. **Azure Production Deployment:** Comprehensive Infrastructure-as-Code (IaC) instructions and Azure CLI commands to deploy Azure Data Factory, Azure SQL Database, Storage Accounts, and configure Power BI DirectQuery/Import connections.

---

## 2. Local Zero-Cloud Execution Guide

### 2.1 Prerequisites
- Python 3.10+ (standard libraries + `pandas`, `numpy`, `matplotlib`)
- Git

### 2.2 Step 1: Install Dependencies
```bash
pip install pandas numpy matplotlib
```

### 2.3 Step 2: Generate Enterprise Retail Data
Generates 120,462 sales rows, 42,640 inventory rows, 1,200 products, 36 stores, 60 suppliers, 10,500 POs, and 5,249 returns with realistic seasonality and controlled 1.5% defects:
```bash
python python/generate_data.py
```

### 2.4 Step 3: Run Unit Tests for Python Data Quality Framework
Verifies that the validation framework passes clean data and accurately catches intentional defects:
```bash
python -m unittest tests/python/test_data_quality.py
```

### 2.5 Step 4: Execute the Full Pipeline & Relational Warehouse
Executes the local relational warehouse pipeline: initializes `stg`, `dw`, and `audit` schemas, executes the data quality gate, merges dimensions, watermarks sales, calculates stockout risk levels, and executes automated SQL integrity assertions:
```bash
python tests/test_pipeline_local.py
```

### 2.6 Step 5: Review Pre-Rendered Power BI Dashboards
Review the high-fidelity dashboard screenshots rendered from real metrics in:
```
power-bi/screenshots/
├── 01_executive_overview.png
├── 02_inventory_intelligence.png
├── 03_sales_analytics.png
├── 04_store_performance.png
├── 05_product_supplier_analysis.png
└── 06_data_pipeline_health.png
```

---

## 3. Azure Cloud Production Deployment Guide

### 3.1 Step 1: Resource Group & Storage Provisioning
```bash
# Set environment variables
RESOURCE_GROUP="rg-clarivens-inventory-prod"
LOCATION="centralindia"
STORAGE_ACCOUNT="saclarivensdatalakeprod"

# 1. Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Create Storage Account (ADLS Gen2 Enabled)
az storage account create \
    --name $STORAGE_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard_LRS \
    --kind StorageV2 \
    --enable-hierarchical-namespace true

# 3. Create Ingestion Container
az storage container create \
    --name raw-data \
    --account-name $STORAGE_ACCOUNT
```

### 3.2 Step 2: Upload Source Files to Data Lake
```bash
# Upload master reference CSVs
az storage blob upload-batch \
    --destination raw-data \
    --source data/ \
    --account-name $STORAGE_ACCOUNT
```

### 3.3 Step 3: Provision Azure SQL Database
```bash
SQL_SERVER="clarivens-sql-server-prod"
SQL_DB="sqldb-clarivens-inventory-prod"
ADMIN_USER="clarivens_admin"

# 1. Create Logical SQL Server
az sql server create \
    --name $SQL_SERVER \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --admin-user $ADMIN_USER \
    --admin-password "ClarivensSecureP@ssw0rd2025!"

# 2. Configure Firewall Rule to Allow Azure Services
az sql server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --server $SQL_SERVER \
    --name "AllowAllWindowsAzureIps" \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

# 3. Create Azure SQL Database (General Purpose 2 vCores)
az sql db create \
    --resource-group $RESOURCE_GROUP \
    --server $SQL_SERVER \
    --name $SQL_DB \
    --service-objective GP_Gen5_2
```

### 3.4 Step 4: Execute SQL Database Migrations
Connect to the database via SQL Server Management Studio (SSMS), Azure Data Studio, or `sqlcmd`, and execute scripts in `sql/` in the following sequence:

1. `sql/database/00_init_database.sql` (Creates `stg`, `dw`, `audit` schemas)
2. `sql/staging/01_staging_tables.sql` (Creates staging landing tables)
3. `sql/warehouse/02_dim_tables.sql` (Creates Star Schema dimensions)
4. `sql/warehouse/03_fact_tables.sql` (Creates Star Schema facts)
5. `sql/audit/04_audit_tables.sql` (Creates audit and watermark control tables)
6. `sql/stored_procedures/*.sql` (Creates all ETL stored procedures)
7. `sql/views/*.sql` (Creates analytical views)
8. `sql/indexes/05_warehouse_indexes.sql` (Applies performance non-clustered indexes)

### 3.5 Step 5: Provision Azure Data Factory
```bash
ADF_NAME="adf-clarivens-inventory-prod"

az datafactory create \
    --resource-group $RESOURCE_GROUP \
    --name $ADF_NAME \
    --location $LOCATION
```

### 3.6 Step 6: Grant ADF Managed Identity Access to Azure SQL
```sql
-- In Azure SQL Database, create a contained database user for ADF Managed Identity
CREATE USER [adf-clarivens-inventory-prod] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [adf-clarivens-inventory-prod];
ALTER ROLE db_datawriter ADD MEMBER [adf-clarivens-inventory-prod];
ALTER ROLE db_ddladmin ADD MEMBER [adf-clarivens-inventory-prod];
GRANT EXECUTE ON SCHEMA::dw TO [adf-clarivens-inventory-prod];
GRANT EXECUTE ON SCHEMA::audit TO [adf-clarivens-inventory-prod];
```

### 3.7 Step 7: Import ADF Artifacts
Import the JSON definitions from `azure-data-factory/` into ADF Studio or deploy via GitHub integration:
1. Deploy Linked Services (`azure-data-factory/linked-services/`)
2. Deploy Datasets (`azure-data-factory/datasets/`)
3. Deploy Pipelines (`azure-data-factory/pipelines/`)
4. Enable Triggers (`azure-data-factory/triggers/`)

### 3.8 Step 8: Connect Power BI to Azure SQL Database
1. Launch **Power BI Desktop**.
2. Select **Get Data** -> **Azure SQL Database**.
3. Server: `clarivens-sql-server-prod.database.windows.net`, Database: `sqldb-clarivens-inventory-prod`.
4. Select `dw.DimDate`, `dw.DimProduct`, `dw.DimStore`, `dw.DimSupplier`, `dw.DimCategory`, `dw.FactSales`, `dw.FactInventory`, `dw.FactPurchases`, `dw.FactReturns`, and `audit.vw_PipelineHealth`.
5. Import `power-bi/theme.json` via **View** -> **Themes** -> **Browse for Themes**.
6. Create DAX measures from `power-bi/dax-measures.md`.
