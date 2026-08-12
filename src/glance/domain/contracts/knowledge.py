from typing import List, Optional
from pydantic import BaseModel, Field

class BeautyKnowledgeReference(BaseModel):
    reference_id: str = Field(..., description="Unique knowledge reference identifier")
    title: str = Field(..., description="Title of the styling guideline or document reference")
    source_url_or_path: str = Field(..., description="Link to source material")
    applicable_style_tags: List[str] = Field(default_factory=list, description="Associated style tags")
    excerpt: Optional[str] = Field(default=None, description="Relevant excerpt text")
