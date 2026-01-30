# Link model for hyperlinks on the page
# Used by Parser to extract navigation options
# Represents <a> tags with href attributes

from typing import Optional, Tuple
from pydantic import BaseModel, Field


class Link(BaseModel):
    text: str = Field(..., description="Visible text content of the link")
    position: Tuple[float, float] = Field(..., description="X, Y coordinates of the link center")
    url: str = Field(..., description="Target URL of the link")
    parent_text: Optional[str] = Field(None, description="Text content of parent container(s)")
    selector: str = Field(..., description="CSS selector or XPath to interact with this link")
    
    class Config:
        frozen = True
