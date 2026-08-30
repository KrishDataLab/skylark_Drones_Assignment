from http.server import BaseHTTPRequestHandler
import json
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
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
        self.wfile.write(json.dumps(res).encode('utf-8'))
