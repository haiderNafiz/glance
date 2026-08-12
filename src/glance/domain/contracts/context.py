from typing import List, Optional
from pydantic import BaseModel, Field
from glance.domain.taxonomy.hair import HairLengthCategory, HairTexture, HairColorFamily
from glance.domain.contracts.base import Confidence

class LearnedHairPreference(BaseModel):
    preferred_lengths: List[HairLengthCategory] = Field(default_factory=list)
    preferred_textures: List[HairTexture] = Field(default_factory=list)
    preferred_colors: List[HairColorFamily] = Field(default_factory=list)
    avoided_styling_tags: List[str] = Field(default_factory=list)
    explicit_likes: List[str] = Field(default_factory=list, description="Style IDs user explicitly liked/saved")
    explicit_dislikes: List[str] = Field(default_factory=list, description="Style IDs user explicitly disliked/rejected")
    confidence: Optional[Confidence] = None
    last_evaluated: Optional[str] = None

class PersonalBeautyContext(BaseModel):
    user_id: Optional[str] = Field(default=None, description="Nullable for anonymous/cold start")
    learned_preferences: LearnedHairPreference = Field(default_factory=LearnedHairPreference)
    last_updated: str = Field(..., description="ISO-8601 updated timestamp")

class BeautyContextUpdate(BaseModel):
    update_id: str = Field(..., description="Unique update ID")
    user_id: str = Field(..., description="Target user profile ID")
    new_likes: List[str] = Field(default_factory=list, description="Visual look IDs to add to explicit likes")
    new_dislikes: List[str] = Field(default_factory=list, description="Visual look IDs to add to explicit dislikes")
    inferred_lengths: List[HairLengthCategory] = Field(default_factory=list, description="New length categories to add")
    inferred_textures: List[HairTexture] = Field(default_factory=list, description="New textures to add")
    inferred_colors: List[HairColorFamily] = Field(default_factory=list, description="New color families to add")
    timestamp_utc: str = Field(..., description="Update processing time")
