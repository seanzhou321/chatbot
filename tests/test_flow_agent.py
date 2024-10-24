import pytest
from crm_chatbot.agents.flow_agent import FlowState, create_flow_agent
from langgraph.graph import StateGraph

def test_create_flow_agent():
    """Test successful flow agent creation"""
    app = create_flow_agent(FlowState)

    assert isinstance(app.builder, StateGraph)