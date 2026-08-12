from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from glance.domain.taxonomy.hair import HairLength, HairTexture, HairColorFamily, HaircutStructure
from glance.domain.contracts.base import Evidence, Provenance
from glance.domain.contracts.perception import HairVisualContext
from glance.domain.contracts.intent import HairLookIntent
from glance.domain.contracts.context import PersonalBeautyContext

class HairLook(BaseModel):
    look_id: str = Field(..., description="Unique identifier for this specific visual look layout")
    name: str = Field(..., description="Name of the style")
    length: HairLength = Field(..., description="Target length category, landmark, and optional cm")
    texture: HairTexture = Field(..., description="Target hair texture type")
    color: HairColorFamily = Field(..., description="Target color family")
    styling_tags: List[str] = Field(default_factory=list, description="Style labels")
    haircut_structure: HaircutStructure = Field(..., description="Fundamental cutting geometry")
    description: str = Field(..., description="Textual description explaining the look visual appearance")

class RecommendationRequest(BaseModel):
    request_id: str = Field(..., description="Unique tracking identifier")
    user_id: Optional[str] = Field(default=None, description="Optional user reference")
    current_intent: HairLookIntent = Field(..., description="Structured user intent request")
    visual_context: Optional[HairVisualContext] = Field(default=None, description="Optional visually inferred context")
    personal_context: Optional[PersonalBeautyContext] = Field(default=None, description="Optional stable preferences")

class RecommendationCandidate(BaseModel):
    candidate_id: str = Field(..., description="Unique proposal ID")
    look: HairLook = Field(..., description="The product-independent visual style")
    ranking_score: float = Field(..., ge=0.0, le=1.0, description="Score between 0.0 and 1.0 indicating suitability rating")
    matching_reasoning: str = Field(..., description="Reasoning explaining why this look fits request")
    evidence: Evidence = Field(default_factory=Evidence, description="Context evidence supporting alignment")

class RecommendationResponse(BaseModel):
    response_id: str = Field(..., description="Unique response tracking ID")
    request_id: str = Field(..., description="Reference back to the request")
    candidates: List[RecommendationCandidate] = Field(..., description="Ordered recommendation candidates")
    provenance: Provenance = Field(..., description="Processing node information")

    @field_validator("candidates")
    @classmethod
    def validate_candidate_count(cls, v: List[RecommendationCandidate]) -> List[RecommendationCandidate]:
        if not (1 <= len(v) <= 5):
            raise ValueError("RecommendationResponse must contain between 1 and 5 candidates.")
        return v

class BeautyFeedback(BaseModel):
    feedback_id: str = Field(..., description="Unique feedback record ID")
    user_id: Optional[str] = Field(default=None, description="Reference to feedback provider")
    look_id: str = Field(..., description="Identifier of the look being rated")
    response_id: str = Field(..., description="ID of the recommendation interaction session")
    rating: int = Field(..., ge=1, le=5, description="Rating score on scale of 1 to 5")
    comments: Optional[str] = Field(default=None, description="Feedback text comments")
    timestamp_utc: str = Field(..., description="Timestamp feedback was received")
