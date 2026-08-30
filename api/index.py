from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import asyncio

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

_agent = None

def get_agent():
    global _agent
    if _agent is None:
        from backend.agent.bi_agent import BIAgent
        _agent = BIAgent()
    return _agent

def run_async_query(query: str):
    ag = get_agent()
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    return loop.run_until_complete(ag.process_query(query))

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Skylark Drones — Monday.com BI Agent</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-950 text-slate-100 antialiased font-outfit">
    <div id="root"></div>
  </body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            path = self.path
            if 'favicon' in path or 'ico' in path:
                self.send_response(204)
                self.end_headers()
                return
            elif 'health' in path:
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
                dist_html = os.path.join(root_dir, 'frontend', 'dist', 'index.html')
                if os.path.exists(dist_html):
                    with open(dist_html, 'rb') as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(INDEX_HTML.encode('utf-8'))
        except Exception:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode('utf-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception:
            req_data = {}
            
        raw_q = req_data.get('query', '')
        
        try:
            result = run_async_query(raw_q)
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
