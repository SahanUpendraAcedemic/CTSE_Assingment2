from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from .prompts import FACT_CHECKER_SYSTEM_PROMPT
from .tools import verify_fact_wikipedia

def get_fact_checker_agent():
    """
    Initializes the local Llama3.1 model and creates a ReAct agent 
    capable of autonomously running tools in a loop.
    """
    # Initialize the local LLM
    llm = ChatOllama(model="llama3.1", temperature=0.2)
    
    # List the tools the agent is allowed to use
    tools = [verify_fact_wikipedia]
    
    # create_react_agent automatically builds the LangGraph logic to handle tool calling!
    agent_executor = create_react_agent(
        llm, 
        tools, 
        prompt=FACT_CHECKER_SYSTEM_PROMPT
    )
    return agent_executor

def fact_checker_node(state: dict) -> dict:
    """
    Wrapper node to execute the agent and parse the results.
    """
    # 1. Look for 'search_results' instead of 'research_data'
    research_to_check = state.get("search_results", "")
    agent = get_fact_checker_agent()
    
    inputs = {
        "messages": [("user", f"Please verify this research: {research_to_check}")]
    }
    
    result = agent.invoke(inputs)
    final_answer = result["messages"][-1].content
    
    # 2. Save the output to 'verified_claims' so the rest of the app can find it
    return {"verified_claims": final_answer}