from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import asyncio

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.agent.bi_agent import BIAgent

agent = BIAgent()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        dist_html = os.path.join(root_dir, 'frontend', 'dist', 'index.html')
        path = self.path
        if 'health' in path:
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
            body = json.dumps(res, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)
        else:
            if os.path.exists(dist_html):
                with open(dist_html, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content)
            else:
                res = {
                    "status": "online",
                    "app": "Skylark Drones Monday.com BI Agent",
                    "version": "1.0.0"
                }
                body = json.dumps(res).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(body)

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception:
            req_data = {}
            
        raw_q = req_data.get('query', '')
        
        try:
            # Delegate directly to deterministic BI Engine
            result = asyncio.run(agent.process_query(raw_q))
            res = result.model_dump()
        except Exception as err:
            res = {
                "query": raw_q,
                "direct_answer": f"Error executing query: {str(err)}",
                "intent": {"metric": "error", "dimensions": []},
                "key_numbers": {},
                "insights": [],
                "data_notes": [f"Execution error: {str(err)}"],
                "execution_trace": [f"Error: {str(err)}"]
            }
            
        body = json.dumps(res, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

app = handler
