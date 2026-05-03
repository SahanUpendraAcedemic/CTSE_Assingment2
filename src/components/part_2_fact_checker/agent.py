from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from .tools import verify_fact_wikipedia
import json

# We update the prompt to explicitly tell the model HOW to use the tool
FACT_CHECKER_SYSTEM_PROMPT = """
You are a meticulous Senior Information Auditor. Your goal is to fact-check research.
If you need to verify a fact, you MUST output a JSON object in exactly this format:
{"action": "search_wikipedia", "query": "your search term here"}

If you have verified the facts and are ready to output the final corrected text, 
output it normally as plain text. Do not output JSON when providing the final answer.
"""

def fact_checker_node(state: dict) -> dict:
    """
    Custom ReAct loop that manually handles tool calling for models
    that do not support native LangChain tool binding (like phi3).
    """
    research_to_check = state.get("search_results", "")
    
    # We use the lightweight phi3 model
    llm = ChatOllama(model="phi3", temperature=0.2)
    
    messages = [
        SystemMessage(content=FACT_CHECKER_SYSTEM_PROMPT),
        HumanMessage(content=f"Please verify this research:\n{research_to_check}")
    ]
    
    # We will let the agent loop up to 3 times to gather facts
    max_loops = 3
    
    for i in range(max_loops):
        print(f"   [Agent 2 Loop {i+1}] Thinking...")
        response = llm.invoke(messages)
        content = response.content
        
        # Check if the model is trying to call our tool
        if '{"action": "search_wikipedia"' in content:
            try:
                # Extract the JSON command from the text
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                command = json.loads(json_str)
                
                query = command.get("query", "")
                print(f"   [Agent 2] Searching Wikipedia for: '{query}'")
                
                # Run the tool
                tool_result = verify_fact_wikipedia.invoke({"query": query})
                
                # Add the tool result back into the conversation history
                messages.append(response) # Add the AI's request
                messages.append(HumanMessage(content=f"Tool Result:\n{tool_result}"))
                
            except json.JSONDecodeError:
                messages.append(HumanMessage(content="Error parsing your JSON tool request. Please format exactly as requested."))
        else:
            # If no tool is requested, the model has output the final answer!
            print("   [Agent 2] Final fact-check complete.")
            return {"verified_claims": content}
            
    # Fallback if it loops too many times without finishing
    return {"verified_claims": "Fact-checker timed out. Here is the partial result:\n" + content}