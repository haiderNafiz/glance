import re
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class Confidence(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="Certainty score of the observation itself")

class EvidenceSourceType(str, Enum):
    USER_DECLARED = "USER_DECLARED"
    IMAGE_OBSERVED = "IMAGE_OBSERVED"
    SYSTEM_INFERRED = "SYSTEM_INFERRED"
    HISTORICAL_FEEDBACK = "HISTORICAL_FEEDBACK"
    KNOWLEDGE_DERIVED = "KNOWLEDGE_DERIVED"

class EvidenceItem(BaseModel):
    source_type: EvidenceSourceType
    segment_text: Optional[str] = Field(default=None, description="Text segment backing the observation")
    bounding_box: Optional[List[float]] = Field(default=None, description="Visual region coordinates [x1, y1, x2, y2]")
    description: str = Field(..., description="Explanation of backing evidence")
    confidence: Confidence

    @field_validator("bounding_box")
    @classmethod
    def validate_bounding_box(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        if v is not None:
            if len(v) != 4:
                raise ValueError("Bounding box must contain exactly 4 coordinates [x1, y1, x2, y2]")
            for coord in v:
                if coord < 0.0:
                    raise ValueError("Bounding box coordinates must be positive floats")
        return v

class Evidence(BaseModel):
    items: List[EvidenceItem] = Field(default_factory=list)

class Provenance(BaseModel):
    service_name: str = Field(..., description="System component identifier")
    version: str = Field(..., description="Component version")
    timestamp_utc: str = Field(..., description="Inference timestamp")
    source_reliability_score: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Optional reliability coefficient")

class ImageReference(BaseModel):
    image_id: str = Field(..., description="Unique identifier for the image asset")
    url_or_path: str = Field(..., description="Path or location of image file; base64 strings are explicitly rejected")
    timestamp_utc: str = Field(..., description="Timestamp of image capture/upload")

    @field_validator("url_or_path")
    @classmethod
    def reject_base64(cls, v: str) -> str:
        # Check for data URI base64 headers or general raw base64 character patterns
        if v.strip().lower().startswith("data:") or "base64" in v.lower() or re.match(r"^[a-zA-Z0-9+/=]{50,}$", v.strip()):
            raise ValueError("Raw image bytes or base64 data strings are not allowed in ImageReference.")
        return v
