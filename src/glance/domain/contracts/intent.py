from typing import List
from pydantic import BaseModel, Field
from glance.domain.taxonomy.hair import HairLengthCategory, HairTexture, HairColorFamily
from glance.domain.contracts.base import Evidence

class HairLookIntent(BaseModel):
    intent_id: str = Field(..., description="Unique intent state tracking ID")
    raw_user_prompt: str = Field(..., description="The original natural language query from the user")
    desired_length: HairLengthCategory = HairLengthCategory.UNKNOWN
    desired_texture: HairTexture = HairTexture.UNKNOWN
    desired_color: HairColorFamily = HairColorFamily.UNKNOWN
    desired_style_tags: List[str] = Field(default_factory=list, description="Specific styling keywords requested")
    avoid_tags: List[str] = Field(default_factory=list, description="Explicit avoidances/exclusions")
    evidence: Evidence = Field(default_factory=Evidence)
