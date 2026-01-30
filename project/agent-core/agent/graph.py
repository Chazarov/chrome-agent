from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage
from playwright.async_api import Page

from .state import AgentState
from .llm import get_llm
from .tools_config import create_agent_tools


SYSTEM_PROMPT = """You are a browser automation agent. Your job is to help users complete tasks on the web.

You have access to the following capabilities:
- Navigate to URLs
- Get information about the current page (buttons, links, text)
- Click on buttons and links
- Type text into input fields
- Scroll the page
- Navigate browser history

When given a task:
1. First, get information about the current page to understand what's available
2. Plan your actions based on the page content
3. Execute actions step by step
4. Verify results after each action
5. Continue until the task is complete

Important guidelines:
- Always check the page content before taking actions
- Use descriptive selectors to interact with elements
- Be specific about which button or link to click
- If something fails, try alternative approaches
- Ask for clarification if the task is ambiguous

When the task is complete, clearly state what was accomplished."""


def create_agent_graph(page: Page, api_key: str):
    """
    Create the LangGraph agent for browser automation
    
    Args:
        page: Playwright page instance
        api_key: Groq API key
        
    Returns:
        Compiled StateGraph
    """
    
    # Initialize LLM and tools
    llm = get_llm(api_key)
    tools = create_agent_tools(page)
    llm_with_tools = llm.bind_tools(tools)
    
    # Create tool node
    tool_node = ToolNode(tools)
    
    # Define agent node
    async def agent_node(state: AgentState) -> AgentState:
        """Main agent reasoning node"""
        messages = state["messages"]
        
        # Add system prompt if first message
        if len(messages) == 1:
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
        # Call LLM
        response = await llm_with_tools.ainvoke(messages)
        
        return {
            "messages": [response],
            "completed": False,
            "error": None
        }
    
    # Define completion check node
    async def check_completion(state: AgentState) -> AgentState:
        """Check if task is completed"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # Simple heuristic: if agent doesn't call tools, consider task done
        if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
            return {"completed": True}
        
        return {"completed": False}
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("check_completion", check_completion)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges from agent
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: "check_completion"
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Add edge from completion check to end
    workflow.add_edge("check_completion", END)
    
    # Compile graph
    return workflow.compile()
