from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from langchain.schema import Document
from .main_chain import main_prompt_template, main_chain
from .hallucination_grader import hallucination_grader
from .web_search import web_search_tool


### State


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        prompt: prompt
    """

    location: str
    generation: str
    prompt: str
    documents: str

def generate(state):
    print("---GENERATE---")
    location = state["location"]
    documents = state["documents"]

    # generation
    generation = main_chain.invoke({"location": location, "document": documents})
    prompt = main_prompt_template.format(location=location, document=documents)

    return {"prompt": prompt, "location": location, "generation": generation, "documents": documents}

def grade_generation_v_question(state):

    print("---CHECK HALLUCINATIONS---")
    location = state["location"]
    prompt = state["prompt"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"prompt": prompt, "generation": generation}
    )
    grade = score["score"]
    # Check hallucination
    if grade == "yes":
        print("---DECISION: GENERATION ALIGNS WITH THE QUESTION---")
        return "useful"
    else:
        print("---DECISION: GENERATION DOES NOT ALIGNS WITH THE QUESTION---")
        return "not useful"


def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")
    location = state["location"]
    documents = state["documents"]

    # Web search
    docs = web_search_tool.invoke({"query": location})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "location": location}

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search)  # web search
workflow.add_node("generate", generate)  # generatae

# Build graph
workflow.set_entry_point("generate")
workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_question,
    {
        "useful": END,
        "not useful": "websearch",
    },
)

# Compile
main_app = workflow.compile()