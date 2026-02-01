from typing import Literal, TYPE_CHECKING
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage
from playwright.async_api import Page

from config import config
from .state import AgentState
from .llm import get_llm
from .tools_config import create_agent_tools
from .debug_tools import print_llm_response, log_error, extract_reasoning
from exceptions.function_call_format import FunctionCallFormatError

if TYPE_CHECKING:
    from parser.browser_manager import BrowserManager


SYSTEM_PROMPT = """You are a browser automation agent that helps users complete web tasks.

## Available Tools

**Navigation:**
- navigate(url) - Go to a URL
- go_back() - Navigate back in browser history

**Page Information (Paginated):**
- get_page_buttons_next_item() - Get next batch of buttons and inputs with unique IDs
  Returns: {buttons: [{id, text, position, parent_text}], inputs: [{id, input_type, name, placeholder, position}]}
- get_page_links_next_item() - Get next batch of 20 links
  Returns: {links: [{text, url, parent_text}]}
- get_page_text_next_item() - Get next 700 characters of page text
  Returns: {text_chunk, item_id, total_items}

**Actions:**
- click_button(button_id) - Click button using ID from get_page_buttons_next_item
- fill_input(input_id, text) - Fill input (clears first) using ID from get_page_buttons_next_item
- type_text(input_id, text) - Type into input (appends) using ID from get_page_buttons_next_item
- press_key(key) - Press keyboard key: "Enter" (submit), "Tab" (next field), "Escape" (close), "ArrowDown"/"ArrowUp" (navigate)

## Important Rules

1. **Pagination**: Page info tools return data in chunks. Call them repeatedly until you get "All items have been retrieved" message to see all elements.

2. **ID-Based Interaction**: ALWAYS use element IDs from get_page_buttons_next_item for click_button, fill_input, and type_text. Never use selectors or text.

3. **URL Usage**: Use URLs from links with navigate() tool, not click_button.

## Typical Workflow

1. After navigation, call get_page_buttons_next_item to see available actions
2. If you need to see more elements, call get_page_buttons_next_item again (repeat until complete)
3. For navigation options, call get_page_links_next_item
4. To read content, call get_page_text_next_item
5. Use element IDs to interact: click_button(id), fill_input(id, "text"), type_text(id, "text")
6. After actions, re-fetch page info to see changes

## Examples

Finding and clicking a login button:
1. get_page_buttons_next_item() → see buttons with IDs
2. click_button(5) → click the button with id=5

Filling a form:
1. get_page_buttons_next_item() → get input field IDs
2. fill_input(2, "user@email.com") → fill email input
3. fill_input(3, "password123") → fill password input
4. click_button(4) → submit form

Searching on a website:
1. get_page_buttons_next_item() → find search input ID
2. fill_input(6, "search query") → fill search box
3. press_key("Enter") → submit search
4. get_page_links_next_item() → see search results

When complete, clearly state what was accomplished."""


def create_agent_graph(page: Page, browser_manager: "BrowserManager", api_key: str):
    """
    Create the LangGraph agent for browser automation
    
    Args:
        page: Playwright page instance
        browser_manager: BrowserManager instance for element storage
        api_key: Groq API key
        
    Returns:
        Compiled StateGraph
    """
    
    # Initialize LLM and tools
    llm = get_llm(api_key)
    tools = create_agent_tools(page, browser_manager)
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
        
        # Call LLM with error handling for malformed function calls
        try:
            response = await llm_with_tools.ainvoke(messages)
            
            if config.is_debug():
                print_llm_response(response)
            
            # Collect debug information if enabled
            if config.is_save_debug_info_enabled():
                from .debug_collector import DebugCollector
                collector = DebugCollector.get_instance()
                
                # Collect reasoning
                reasoning_content = extract_reasoning(response)
                if reasoning_content:
                    collector.add_reasoning(reasoning_content)
                
                # Collect tool calls
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    for tool_call in response.tool_calls:
                        collector.add_tool_call(
                            tool_call.get('name', 'unknown'),
                            tool_call.get('args', {})
                        )
                
        except Exception as e:
            error_str = str(e)
            if "400" in error_str and "Failed to call a function" in error_str:
                err = FunctionCallFormatError(details=error_str)
                log_error(err)
                raise err from e
            raise
        
        
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
