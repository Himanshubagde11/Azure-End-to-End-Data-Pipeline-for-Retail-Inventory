"""
CLARIVENS INVENTORY INTELLIGENCE
Mock REST API Server & Data Generator
Author: Senior Data Engineer / Azure Data Architect
Organization: CLARIVENS RETAIL GROUP

Implements a production-style REST API simulating an external Supplier & Market Intelligence Feed:
- Endpoint: /api/v1/supplier-catalog
- Endpoint: /api/v1/products/enrichment
- Authentication: Bearer Token (Authorization: Bearer clarivens-api-prod-key-2025)
- Pagination: page & limit parameters with nextPageUrl and metadata
- Response: JSON format adhering to enterprise REST standards
"""

import os
import json
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import pandas as pd
from config import REST_API_CONFIG, DATA_DIR

def load_catalog_data():
    prod_path = os.path.join(DATA_DIR, "products.csv")
    if os.path.exists(prod_path):
        df = pd.read_csv(prod_path)
        enrichment_records = []
        for _, row in df.iterrows():
            cost = float(row["UnitCost"]) if pd.notna(row["UnitCost"]) else 150.0
            reorder_lvl = int(row["ReorderLevel"]) if pd.notna(row["ReorderLevel"]) else 50
            enrichment_records.append({
                "ProductID": str(row["ProductID"]),
                "SupplierID": str(row["SupplierID"]),
                "LiveReplenishmentPrice": round(cost * random.uniform(0.96, 1.05), 2),
                "RecommendedSafetyStock": int(reorder_lvl * random.uniform(0.9, 1.2)),
                "VendorLeadTimeDays": random.randint(3, 14),
                "SupplyChainRiskScore": round(random.uniform(1.0, 4.5), 1),
                "LastEvaluatedDate": "2025-12-31"
            })
        return enrichment_records
    return []

ENRICHMENT_CACHE = load_catalog_data()

class ClarivensApiRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Clarivens-API-Version", "1.2.0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def _check_auth(self):
        auth_header = self.headers.get("Authorization", "")
        # Accept production key or token alias
        valid_tokens = [
            f"Bearer {REST_API_CONFIG['api_key']}",
            "Bearer clarivens-api-token-2025",
            "Bearer clarivens-api-prod-key-2025"
        ]
        return any(auth_header.strip() == t for t in valid_tokens)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        # Health endpoint (open without auth)
        if path in ["/health", "/api/v1/health", ""]:
            self._set_headers(200)
            resp = {
                "status": "HEALTHY",
                "service": "Clarivens Supplier & Replenishment REST API",
                "environment": "production-simulation",
                "endpoints": [
                    "/api/v1/health",
                    "/api/v1/products/enrichment",
                    "/api/v1/suppliers"
                ],
                "timestamp": "2025-12-31T23:59:59Z"
            }
            self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
            return

        # Check authentication for secure data endpoints
        if not self._check_auth():
            self._set_headers(401)
            resp = {
                "error": "Unauthorized",
                "message": "Invalid or missing Bearer token in Authorization header. Expected: 'Bearer clarivens-api-prod-key-2025' or 'Bearer clarivens-api-token-2025'"
            }
            self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))
            return

        # 1. Product Enrichment & Supplier Catalog Endpoints
        enrichment_paths = [
            REST_API_CONFIG["enrichment_endpoint"].rstrip("/"),
            "/api/v1/suppliers",
            "/api/v1/supplier-catalog"
        ]
        if path in enrichment_paths:
            page = int(query.get("page", [1])[0])
            limit = int(query.get("limit", [100])[0])
            
            total_records = len(ENRICHMENT_CACHE)
            total_pages = (total_records + limit - 1) // limit if limit > 0 else 1
            
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            page_data = ENRICHMENT_CACHE[start_idx:end_idx]

            port = self.server.server_port
            base_url = f"http://localhost:{port}{path}"
            next_url = f"{base_url}?page={page+1}&limit={limit}" if page < total_pages else None
            prev_url = f"{base_url}?page={page-1}&limit={limit}" if page > 1 else None

            payload = {
                "metadata": {
                    "totalRecords": total_records,
                    "pageSize": limit,
                    "currentPage": page,
                    "totalPages": total_pages,
                    "nextPageUrl": next_url,
                    "previousPageUrl": prev_url
                },
                "data": page_data
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
            return

        # 404 handler
        self._set_headers(404)
        resp = {"error": "Not Found", "message": f"Endpoint '{path}' is not registered."}
        self.wfile.write(json.dumps(resp, indent=2).encode("utf-8"))

def export_enrichment_snapshot(output_file=None):
    """
    Direct exporter for testing or offline ingestion simulation
    """
    if not output_file:
        output_file = os.path.join(DATA_DIR, "rest_api_enrichment_feed.json")
    with open(output_file, "w") as f:
        json.dump({
            "metadata": {"source": "REST_API", "totalRecords": len(ENRICHMENT_CACHE)},
            "data": ENRICHMENT_CACHE
        }, f, indent=2)
    print(f"Mock REST API Enrichment Snapshot saved to {output_file} ({len(ENRICHMENT_CACHE)} records)")

def run_server(host=None, port=None):
    if host is None:
        host = REST_API_CONFIG["host"]
    if port is None:
        port = REST_API_CONFIG["port"]
    server = HTTPServer((host, port), ClarivensApiRequestHandler)
    print(f"===========================================================")
    print(f" CLARIVENS REST API SERVER RUNNING on http://localhost:{port}")
    print(f" Health Check: http://localhost:{port}/health")
    print(f" Enrichment:   http://localhost:{port}/api/v1/products/enrichment?page=1&limit=10")
    print(f" Suppliers:    http://localhost:{port}/api/v1/suppliers?page=1&limit=10")
    print(f" Auth Header:  Authorization: Bearer {REST_API_CONFIG['api_key']}")
    print(f" Press Ctrl+C to stop the server")
    print(f"===========================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down REST API server...")
        server.server_close()

if __name__ == "__main__":
    import sys
    port = REST_API_CONFIG["port"]
    if "--port" in sys.argv:
        try:
            port_idx = sys.argv.index("--port") + 1
            port = int(sys.argv[port_idx])
        except (IndexError, ValueError):
            pass

    if "--export-only" in sys.argv:
        export_enrichment_snapshot()
    else:
        export_enrichment_snapshot()
        run_server(port=port)

