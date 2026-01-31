from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel

from config import config


def get_llm(api_key: Optional[str] = None) -> BaseChatModel:
    """
    Initialize Groq LLM
    
    Args:
        api_key: Groq API key (defaults to config.groq_api_key)
        
    Returns:
        Initialized ChatGroq instance
    """
    if api_key is None:
        api_key = config.groq_api_key
        
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in configuration")
    
    return ChatGroq(
        model=config.agent_model,
        api_key=api_key,
        temperature=config.agent_temperature,
        max_tokens=config.agent_max_tokens
    )
