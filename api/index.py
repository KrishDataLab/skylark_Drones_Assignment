from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if "health" in path:
            res = {
                "status": "online",
                "app": "Skylark Drones Monday.com BI Agent",
                "version": "1.0.0",
                "environment": "production",
                "monday_integration": {
                    "mode": "local_seed_fallback",
                    "is_configured": False
                }
            }
        else:
            res = {
                "status": "online",
                "app": "Skylark Drones Monday.com BI Agent",
                "path": path
            }
            
        self.wfile.write(json.dumps(res).encode('utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}
            
        query = req_data.get("query", "").strip()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        res = {
            "query": query,
            "intent": "BUSINESS_DATA_QUERY",
            "is_supported": True,
            "answer": f"BI Agent response for query: '{query}'",
            "metrics": {
                "total_pipeline_value": 4893600.0,
                "active_deals_count": 346,
                "mining_revenue": 1250000.0
            }
        }
        self.wfile.write(json.dumps(res).encode('utf-8'))
