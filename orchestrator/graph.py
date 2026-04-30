from langgraph.graph import StateGraph, END
from typing import TypedDict, Any, Annotated
from services import call
from common.llm import call_llm
from config import CONFIG
from operator import add

PLANNER = "http://planner:8001/plan"
RETRIEVER = "http://retriever:8000/retrieve"
MEMORY = "http://memory:8003/get"
CRITIC = "http://critic:8005/critic"
SAFETY = "http://safety:8006/safety"

MAX_CRITIC_LOOPS = 3
MAX_SAFETY_LOOPS = 3

class StateSchema(TypedDict):
    query: str
    plan: Any
    context: Any
    memories: Any
    answer: str
    critic_score: float
    critic_feedback: str
    critic_loops: int
    safety_score: float
    safety_feedback: str
    safety_loops: int

async def planner_node(state):
    res = await call(PLANNER, state)
    return {"plan": res["plan"]}

async def retriever_node(state):
    res = await call(RETRIEVER, state)
    return {"context": res["context"]}

async def memory_node(state):
    res = await call(MEMORY, state)
    return {"memories": res["memories"]}

from common.llm import call_llm
from config import CONFIG

async def solution_node(state):
    answer = f"""
Query: {state['query']}

Plan: {state.get('plan')}
Context: {state.get('context')}
Memory: {state.get('memories')}

Critic Feedback:
{state.get('critic_feedback')}

Safety Feedback:
{state.get('safety_feedback')}
"""

    return {"answer": answer}

async def critic_node(state):
    prompt = f"Evaluate:\n{state['answer']}"

    text = await call_llm(
        CONFIG["critic"]["provider"],
        CONFIG["critic"]["model"],
        prompt
    )

    # parse score (simplified)
    return {
        "critic_score": 0.8 if "improve" in text else 0.95,
        "critic_feedback": text
    }

def critic_router(state):
    if state.get("critic_score", 1) < 0.85 and state.get("critic_loops", 0) < MAX_CRITIC_LOOPS:
        return "solution"
    return "safety"

def safety_router(state):
    if state.get("safety_score", 1) < 0.9 and state.get("safety_loops", 0) < MAX_SAFETY_LOOPS:
        return "solution"
    return END    

async def safety_node(state):
    prompt = f"Check safety:\n{state['answer']}"

    text = await call_llm(
        CONFIG["safety"]["provider"],
        CONFIG["safety"]["model"],
        prompt
    )

    return {
        "safety_score": 0.9,
        "safety_feedback": text
    }


def build():
    g = StateGraph(StateSchema)

    g.add_node("planner", planner_node)
    g.add_node("retriever", retriever_node)
    g.add_node("memory", memory_node)
    g.add_node("solution", solution_node)
    g.add_node("critic", critic_node)
    g.add_node("safety", safety_node)

    g.set_entry_point("planner")

    # Sequential flow: planner -> retriever -> memory -> solution
    g.add_edge("planner", "retriever")
    g.add_edge("retriever", "memory")
    g.add_edge("memory", "solution")

    g.add_edge("solution", "critic")
    g.add_edge("critic", "safety")

    g.add_conditional_edges("critic", critic_router)
    g.add_conditional_edges("safety", safety_router)    

    return g.compile()