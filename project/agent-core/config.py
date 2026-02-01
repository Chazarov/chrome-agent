"""
Central configuration module for Chrome Agent.
All environment variables and application settings are managed here.
"""

import os
from enum import Enum
from typing import Optional
from dotenv import load_dotenv


class AppMode(Enum):
    """Application execution mode"""
    DEBUG = "DEBUG"
    PRODUCTION = "PRODUCTION"


class Config:
    """
    Central configuration class for the application.
    Loads and validates all environment variables and settings.
    """
    
    def __init__(self):
        load_dotenv()
        
        self.mode = AppMode.PRODUCTION
        
        self.groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
        
        self.database_path: str = "agent_sessions.db"
        
        self.browser_viewport_width: int = 720
        self.browser_viewport_height: int = 720
        self.browser_timeout: int = 30000 
        
        self.agent_model: str = "openai/gpt-oss-20b"  # Production model with tool calling
        self.agent_temperature: float = 0.7
        self.agent_max_tokens: int = 2048
        self.agent_max_retries: int = 3
        self.agent_max_steps: int = 50
        self.agent_reasoning_effort: str = "high"
        
        self.save_debug_info: bool = True  # Enable for debugging: True
    
    def validate(self) -> None:
        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables. "
                "Please create .env file and add: GROQ_API_KEY=your_key_here"
            )
    
    def is_debug(self) -> bool:
        return self.mode == AppMode.DEBUG
    
    def is_production(self) -> bool:
        return self.mode == AppMode.PRODUCTION
    
    def is_save_debug_info_enabled(self) -> bool:
        return self.save_debug_info
    
    def __repr__(self) -> str:
        return (
            f"Config(mode={self.mode.value}, "
            f"model={self.agent_model}, "
            f"database={self.database_path})"
        )


config = Config()
