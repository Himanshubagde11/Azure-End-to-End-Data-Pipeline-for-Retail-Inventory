"""
CLARIVENS INVENTORY INTELLIGENCE
Configuration & Quality Thresholds
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SALES_DIR = os.path.join(DATA_DIR, "sales")
INVENTORY_DIR = os.path.join(DATA_DIR, "inventory")
PURCHASES_DIR = os.path.join(DATA_DIR, "purchases")
RETURNS_DIR = os.path.join(DATA_DIR, "returns")
LOGS_DIR = os.path.join(BASE_DIR, "audit_logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Azure SQL Database / Local SQLite connection settings
# In cloud production, these values are populated from Azure Key Vault or Environment variables
AZURE_SQL_CONFIG = {
    "server": os.getenv("AZURE_SQL_SERVER", "clarivens-sql-server-prod.database.windows.net"),
    "database": os.getenv("AZURE_SQL_DATABASE", "sqldb-clarivens-inventory-prod"),
    "username": os.getenv("AZURE_SQL_USERNAME", "clarivens_admin"),
    "password": os.getenv("AZURE_SQL_PASSWORD", "PLACEHOLDER_SECRET_STORED_IN_KEY_VAULT"),
    "driver": "{ODBC Driver 18 for SQL Server}",
    "encrypt": "yes",
    "trust_server_certificate": "no",
    "timeout": 30
}

# Local relational test database (SQLite file replicating T-SQL schemas for local zero-cloud runs)
LOCAL_DB_PATH = os.path.join(LOGS_DIR, "clarivens_warehouse_local.db")

# Mock REST API Configuration
REST_API_CONFIG = {
    "host": "127.0.0.1",
    "port": 8080,
    "api_key": "clarivens-api-prod-key-2025",
    "catalog_endpoint": "/api/v1/supplier-catalog",
    "enrichment_endpoint": "/api/v1/products/enrichment"
}

# Data Quality Thresholds
DQ_THRESHOLDS = {
    "PASS_THRESHOLD_PCT": 98.0,      # Green: >= 98% records pass
    "WARNING_THRESHOLD_PCT": 95.0,   # Amber: 95% - 98% records pass
    "CRITICAL_FAILURE_PCT": 95.0     # Red: < 95% records pass (pipeline alert / halt)
}

# Master Schemas Definition for Validation
EXPECTED_SCHEMAS = {
    "categories": {
        "columns": ["CategoryID", "CategoryName", "Department"],
        "types": {"CategoryID": "object", "CategoryName": "object", "Department": "object"},
        "primary_key": ["CategoryID"],
        "not_null": ["CategoryID", "CategoryName"]
    },
    "stores": {
        "columns": ["StoreID", "StoreName", "City", "State", "Region", "StoreType", "OpeningDate", "Manager", "SquareFeet", "IsActive"],
        "types": {"StoreID": "object", "StoreName": "object", "City": "object", "SquareFeet": "int64", "IsActive": "int64"},
        "primary_key": ["StoreID"],
        "not_null": ["StoreID", "StoreName", "City", "State", "Region", "StoreType"]
    },
    "suppliers": {
        "columns": ["SupplierID", "SupplierName", "ContactName", "Email", "Phone", "City", "State", "Rating", "PaymentTerms", "LeadTimeDays", "IsActive"],
        "types": {"SupplierID": "object", "SupplierName": "object", "Rating": "float64", "LeadTimeDays": "int64", "IsActive": "int64"},
        "primary_key": ["SupplierID"],
        "not_null": ["SupplierID", "SupplierName", "LeadTimeDays"]
    },
    "products": {
        "columns": ["ProductID", "ProductName", "CategoryID", "CategoryName", "SupplierID", "Brand", "UnitCost", "UnitPrice", "ReorderLevel", "ReorderQuantity", "LaunchDate", "IsActive"],
        "types": {"ProductID": "object", "UnitCost": "float64", "UnitPrice": "float64", "ReorderLevel": "int64", "ReorderQuantity": "int64"},
        "primary_key": ["ProductID"],
        "not_null": ["ProductID", "ProductName", "CategoryID", "SupplierID", "UnitPrice", "UnitCost"]
    },
    "sales": {
        "columns": ["SaleID", "SaleDate", "StoreID", "ProductID", "Quantity", "UnitPrice", "Discount", "Revenue", "Cost", "PaymentMethod", "CustomerSegment"],
        "types": {"SaleID": "object", "SaleDate": "object", "StoreID": "object", "ProductID": "object", "Quantity": "int64", "UnitPrice": "float64", "Discount": "float64", "Revenue": "float64", "Cost": "float64"},
        "primary_key": ["SaleID"],
        "not_null": ["SaleID", "SaleDate", "StoreID", "ProductID", "Quantity", "UnitPrice", "Revenue"]
    },
    "inventory": {
        "columns": ["InventoryID", "SnapshotDate", "StoreID", "ProductID", "OpeningStock", "ReceivedQuantity", "SoldQuantity", "ReturnQuantity", "ClosingStock", "DamagedQuantity", "InventoryValue"],
        "types": {"InventoryID": "object", "SnapshotDate": "object", "OpeningStock": "int64", "ClosingStock": "int64", "InventoryValue": "float64"},
        "primary_key": ["InventoryID"],
        "not_null": ["InventoryID", "SnapshotDate", "StoreID", "ProductID", "ClosingStock", "InventoryValue"]
    },
    "purchases": {
        "columns": ["PurchaseOrderID", "OrderDate", "SupplierID", "StoreID", "ProductID", "OrderedQuantity", "ReceivedQuantity", "UnitCost", "ExpectedDeliveryDate", "ActualDeliveryDate", "Status"],
        "types": {"PurchaseOrderID": "object", "OrderedQuantity": "int64", "ReceivedQuantity": "int64", "UnitCost": "float64"},
        "primary_key": ["PurchaseOrderID"],
        "not_null": ["PurchaseOrderID", "OrderDate", "SupplierID", "StoreID", "ProductID", "OrderedQuantity", "UnitCost"]
    },
    "returns": {
        "columns": ["ReturnID", "ReturnDate", "SaleID", "StoreID", "ProductID", "Quantity", "ReturnReason", "RefundAmount"],
        "types": {"ReturnID": "object", "Quantity": "int64", "RefundAmount": "float64"},
        "primary_key": ["ReturnID"],
        "not_null": ["ReturnID", "ReturnDate", "SaleID", "StoreID", "ProductID", "Quantity", "RefundAmount"]
    }
}
