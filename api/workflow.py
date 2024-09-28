from typing import Literal
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import RetryPolicy

from api.state_fn import summary, aggressive_summary


ANSWER_NODE = "[LLM] answer"


def retry_on_llm_error(exc: Exception) -> bool:
    if isinstance(exc, OutputParserException):
        return True
    if isinstance(exc, Exception) and "InvokeModel" in str(exc):
        return True

def build_answer_workflow() -> CompiledStateGraph:
    llm_failed_retry_policy = RetryPolicy(max_attempts=5, retry_on=retry_on_llm_error)

    workflow = StateGraph(State)

    # Add the nodes to the graph

    workflow.add_node(ANSWER_NODE, summary, retry=llm_failed_retry_policy)
    # Add the edges
    workflow.add_edge(START, ANSWER_NODE)
    workflow.add_edge(ANSWER_NODE, END)

    return workflow.compile()