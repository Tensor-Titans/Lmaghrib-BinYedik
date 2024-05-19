from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from langchain.schema import Document
from .product_price_chain import product_price_chain
from .web_search import web_search_tool

query = "whats the price of 1 kg of sugar in morocco"
documents = None

docs = web_search_tool.invoke({"query": query})
web_results = "\n".join([d["content"] for d in docs])
web_results = Document(page_content=web_results)
if documents is not None:
    documents.append(web_results)
else:
    documents = [web_results]


class GraphState(TypedDict):

    question: str
    generation: str
    documents: str
    history: str


def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]
    history = state["history"]

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question, "history": history}


def generate(state):
    print("---GENERATE---")
    question = state["question"]
    history = state["history"]
    documents = state["documents"]

    # generation
    generation = product_price_chain.invoke(
        {"question": question, "documents": documents, "history": history}
    )

    return {
        "question": question,
        "generation": generation,
        "documents": documents,
    }


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search)  # web search
workflow.add_node("generate", generate)  # generatae

# Build graph
workflow.set_entry_point("websearch")
workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", END)


# Compile
product_price_app = workflow.compile()
