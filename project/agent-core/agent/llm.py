import os
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel


def get_llm(api_key: Optional[str] = None) -> BaseChatModel:
    """
    Initialize Groq LLM with Qwen2.5-VL-7B model
    
    Args:
        api_key: Groq API key (defaults to GROQ_API_KEY env var)
        
    Returns:
        Initialized ChatGroq instance
    """
    if api_key is None:
        api_key = os.getenv("GROQ_API_KEY")
        
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables or parameters")
    
    return ChatGroq(
        model="llama-3.3-70b-versatile",  # Using available model instead of Qwen
        api_key=api_key,
        temperature=0.7,
        max_tokens=2048
    )
