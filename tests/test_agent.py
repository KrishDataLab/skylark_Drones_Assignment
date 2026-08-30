import asyncio
from backend.agent.bi_agent import BIAgent

def test_bi_agent_supported_revenue_query():
    agent = BIAgent()
    res = asyncio.run(agent.process_query("What is our total revenue in mining sector?"))
    assert res.intent.metric == "revenue"
    assert res.intent.sector_filter == "Mining"
    assert res.key_numbers["count"] == 100

def test_bi_agent_supported_pipeline_query():
    agent = BIAgent()
    res = asyncio.run(agent.process_query("What is our current sales pipeline?"))
    assert res.intent.metric == "pipeline"
    assert res.key_numbers["open_deals_count"] == 49

def test_bi_agent_supported_energy_pipeline():
    agent = BIAgent()
    res = asyncio.run(agent.process_query("How's our pipeline looking for energy sector this quarter?"))
    assert res.intent.metric == "pipeline"
    assert res.intent.sector_filter == "Renewable Energy"
    assert res.key_numbers["open_deals_count"] == 8

def test_bi_agent_supported_delayed_work_orders():
    agent = BIAgent()
    res = asyncio.run(agent.process_query("Which work orders are delayed?"))
    assert res.intent.metric == "delayed_work_orders"
    assert res.key_numbers["delayed_count"] == 1

def test_bi_agent_clarification():
    agent = BIAgent()
    res = asyncio.run(agent.process_query("Show me revenue"))
    assert res.intent.needs_clarification
    assert "Would you like" in res.direct_answer

def test_bi_agent_greetings_and_capabilities():
    agent = BIAgent()
    for g in ["hi", "hello", "hey", "what do you do", "what can you do", "how can you help"]:
        res = asyncio.run(agent.process_query(g))
        assert res.intent.metric == "greeting"
        assert "Hello!" in res.direct_answer or "Skylark Drones" in res.direct_answer

def test_bi_agent_unsupported_out_of_domain_queries():
    agent = BIAgent()
    unsupported_list = [
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
    for q in unsupported_list:
        res = asyncio.run(agent.process_query(q))
        assert res.intent.metric == "unsupported_metric"
        assert "I can only answer questions based on Skylark Drones" in res.direct_answer
