from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
import re

from crm_chatbot.tools.llm_choice import instantiate_chatllm

# Initialize LLM. the choices are qwen2.5:14b (9GB), gemma2 (5.4GB), llama3.2 (2GB), and phi3.5 (2.2GB). 
llm = instantiate_chatllm(model="phi3.5", tempreture=0)

# Define our state
class FlowState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], list.append]
    payee: str
    amount: float
    confirmed: bool

# Define our nodes
def collect_info(state: FlowState) -> FlowState:
    messages = state['messages']
    
    if state['payee'] == "":
        prompt = "Please provide the payee's full name."
    elif state['amount'] == 0:
        prompt = f"Please provide the amount to pay {state['payee']}."
    else:
        prompt = f"Please confirm: Pay {state['payee']} the amount of ${state['amount']:.2f}. Is this correct? (Yes/No)"

    llm_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a banking assistant. Collect payment information from the user."),
        ("human", prompt),
        *messages
    ])
    response = llm.invoke(llm_prompt.format())
    state['messages'].append(AIMessage(content=response))
    return state

def validate_info(state: FlowState) -> FlowState:
    if len(state['messages']) > 0:
        user_message = state['messages'][-2].content
        if state['payee'] == "":
            payee_match = re.search(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', user_message)
            if payee_match:
                state['payee'] = payee_match.group()
        elif state['amount'] == 0:
            amount_match = re.search(r'\$?(\d+(\.\d{2})?)', user_message)
            if amount_match:
                state['amount'] = float(amount_match.group(1))
        elif not state['confirmed']:
            if "yes" in user_message.lower():
                state['confirmed'] = True
            elif "no" in user_message.lower():
                state['payee'] = ""
                state['amount'] = 0
    return state

def process_payment(state: FlowState) -> FlowState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a banking assistant. Process the payment and inform the user."),
        ("human", f"Process payment of ${state['amount']:.2f} to {state['payee']}."),
    ])
    response = llm.invoke(prompt.format())
    state['messages'].append(AIMessage(content=response))
    return state

# Define our edges
def router(state: FlowState):
    if not state['confirmed']:
        if state['payee'] == "" or state['amount'] == 0:
            return "collect_info"
        else:
            return "validate_info"
    else:
        return "process_payment"

def create_flow_agent(flowStateCls: FlowState):
    # Create our graph
    workflow = StateGraph(FlowState)

    # Add nodes
    workflow.add_node("collect_info", collect_info)
    workflow.add_node("validate_info", validate_info)
    workflow.add_node("process_payment", process_payment)

    # Add edges
    workflow.add_edge("collect_info", "validate_info")
    workflow.add_conditional_edges("validate_info", router)
    workflow.add_edge("process_payment", END)

    # Set entry point
    workflow.set_entry_point("collect_info")

    # Compile the graph
    app = workflow.compile()
    return app

if __name__ == "__main__":
    # Example usage
    initial_state = {
        "messages": [],
        "payee": "",
        "amount": 0,
        "confirmed": False
    }

    for output in create_flow_agent(FlowState).stream(initial_state):
        if '__end__' not in output:
            response = output['messages'][-1].content
            print(f"Chatbot: {response}")
            user_input = input("User: ")
            output['messages'].append(HumanMessage(content=user_input))
        else:
            print("Transaction completed.")
            break