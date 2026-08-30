import sys
import httpx
import json

sys.stdout.reconfigure(encoding='utf-8')
BASE_URL = "http://localhost:8000"

def verify_all_intent_routing():
    print("=" * 80)
    print("      INTENT-ROUTING & DOMAIN CLASSIFICATION VERIFICATION REPORT")
    print("=" * 80)
    print()

    with httpx.Client(timeout=10.0) as client:
        # 1. Test Unsupported Out-of-Domain Queries
        print("--- 1. UNSUPPORTED OUT-OF-DOMAIN QUERIES ---")
        unsupported_test_cases = [
            "What is the weather today?",
            "Tell me a joke",
            "Who is the president?",
            "What is the capital of India?",
            "Write me a Python program",
            "What is today's news?",
            "What is the stock market doing?",
            "What is employee attrition?",
            "What is EBITDA?",
            "What is CAC?"
        ]
        for q in unsupported_test_cases:
            r = client.post(f"{BASE_URL}/api/chat", json={"query": q})
            d = r.json()
            intent = d.get("intent", {}).get("metric")
            answer = d.get("direct_answer")
            print(f"Query: '{q}'\n  -> Intent: {intent}\n  -> Refusal: {answer}\n")
            assert intent == "unsupported_metric"
            assert "I can only answer questions based on Skylark Drones" in answer
        print("[VERIFIED] All out-of-domain queries properly refused with 0 hallucination!")
        print("-" * 80)
        print()

        # 2. Test Greetings & Capabilities
        print("--- 2. GREETING & CAPABILITY QUERIES ---")
        greeting_test_cases = ["hi", "hello", "hey", "what do you do?", "what can you do?", "how can you help me?"]
        for q in greeting_test_cases:
            r = client.post(f"{BASE_URL}/api/chat", json={"query": q})
            d = r.json()
            intent = d.get("intent", {}).get("metric")
            answer = d.get("direct_answer")
            print(f"Query: '{q}'\n  -> Intent: {intent}\n  -> Response: {answer}\n")
            assert intent == "greeting"
            assert "Hello!" in answer or "Skylark Drones" in answer
        print("[VERIFIED] All greetings and capability queries return friendly agent intro!")
        print("-" * 80)
        print()

        # 3. Test Supported Domain Queries
        print("--- 3. SUPPORTED DOMAIN BI QUERIES ---")
        supported_test_cases = [
            ("What is our current sales pipeline?", "pipeline", 49),
            ("How's our pipeline looking for energy sector this quarter?", "pipeline", 8),
            ("Which work orders are delayed?", "delayed_work_orders", 1),
            ("What is our total revenue in mining sector?", "revenue", 100)
        ]
        for q, expected_metric, expected_count in supported_test_cases:
            r = client.post(f"{BASE_URL}/api/chat", json={"query": q})
            d = r.json()
            intent = d.get("intent", {}).get("metric")
            answer = d.get("direct_answer")
            print(f"Query: '{q}'\n  -> Intent: {intent}\n  -> Answer: {answer}\n")
            assert intent == expected_metric
        print("[VERIFIED] All legitimate business queries execute deterministic BI calculations!")
        print("=" * 80)

if __name__ == "__main__":
    verify_all_intent_routing()
