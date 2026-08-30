from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import sys
import os
import asyncio

# Ensure root directory is in sys.path for Vercel Python Serverless Runtime
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.agent.bi_agent import BIAgent

agent = BIAgent()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
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
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
        
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        try:
            req_data = json.loads(body)
        except Exception:
            req_data = {}
            
        query = req_data.get("query", "").strip()
        
        # Execute BIAgent deterministically
        try:
            result = asyncio.run(agent.process_query(query))
            res = result.dict()
        except Exception as e:
            res = {
                "query": query,
                "direct_answer": f"Error processing query: {str(e)}",
                "intent": {"metric": "error", "needs_clarification": False},
                "key_numbers": {},
                "insights": [],
                "data_notes": ["An error occurred while executing the query calculation."],
                "execution_trace": [f"Execution failed: {str(e)}"]
            }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
