import sys
import httpx
import json

# Force UTF-8 output encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

def verify_live_app():
    print("=" * 80)
    print("      SKYLARK DRONES BI AGENT — LIVE SERVER VERIFICATION REPORT")
    print("=" * 80)
    print()

    with httpx.Client(timeout=10.0) as client:
        # 1. Test Frontend Mount (GET /)
        print("--- 1. FRONTEND STATIC APP (GET /) ---")
        try:
            r_fe = client.get(f"{BASE_URL}/")
            print(f"Status Code : {r_fe.status_code} OK")
            print(f"Content Type: {r_fe.headers.get('content-type')}")
            print(f"HTML Snippet: {r_fe.text[:180].strip()}...")
        except Exception as e:
            print(f"Error connecting to frontend: {e}")
        print("-" * 80)
        print()

        # 2. Test Backend Health Endpoint (GET /api/health)
        print("--- 2. BACKEND HEALTH API (GET /api/health) ---")
        try:
            r_health = client.get(f"{BASE_URL}/api/health")
            print(f"Status Code : {r_health.status_code} OK")
            print(f"JSON Payload: {json.dumps(r_health.json(), indent=2)}")
        except Exception as e:
            print(f"Error connecting to health API: {e}")
        print("-" * 80)
        print()

        # 3. Test Backend Chat API (POST /api/chat)
        print("--- 3. BACKEND BI AGENT CHAT API (POST /api/chat) ---")
        sample_query = "What is our total revenue in mining sector?"
        print(f"User Query  : '{sample_query}'")
        try:
            r_chat = client.post(
                f"{BASE_URL}/api/chat",
                json={"query": sample_query}
            )
            print(f"Status Code : {r_chat.status_code} OK")
            data = r_chat.json()
            print(f"Direct Answer: {data.get('direct_answer')}")
            print(f"Key Numbers  : {json.dumps(data.get('key_numbers'))}")
            print(f"Trace Steps  :")
            for step in data.get("execution_trace", []):
                print(f"  [TRACE] {step}")
        except Exception as e:
            print(f"Error connecting to chat API: {e}")
        print("-" * 80)
        print()

        # 4. Test Backend Leadership Update API (GET /api/export/leadership-update)
        print("--- 4. BACKEND LEADERSHIP REPORT EXPORT API (GET /api/export/leadership-update) ---")
        try:
            r_exp = client.get(f"{BASE_URL}/api/export/leadership-update")
            print(f"Status Code : {r_exp.status_code} OK")
            exp_data = r_exp.json()
            print(f"Report Title: {exp_data.get('report_title')}")
            print(f"Metrics Summary: {json.dumps(exp_data.get('metrics'))}")
        except Exception as e:
            print(f"Error connecting to export API: {e}")
        print("=" * 80)

if __name__ == "__main__":
    verify_live_app()
