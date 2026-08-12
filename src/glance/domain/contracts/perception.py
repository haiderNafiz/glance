from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from glance.domain.taxonomy.hair import (
    HairLength, HairTexture, WavePattern, ApparentVolume,
    ApparentDensity, HairColorFamily, HighlightType, HairLengthCategory
)
from glance.domain.contracts.base import Evidence, EvidenceSourceType, ImageReference, Provenance

class HairVisualContext(BaseModel):
    image_id: str = Field(..., description="Reference to parent image")
    length: HairLength = Field(default_factory=HairLength)
    texture: HairTexture = HairTexture.UNKNOWN
    wave_pattern: WavePattern = WavePattern.UNKNOWN
    apparent_volume: ApparentVolume = ApparentVolume.UNKNOWN
    apparent_density: ApparentDensity = ApparentDensity.UNKNOWN
    color_family: HairColorFamily = HairColorFamily.UNKNOWN
    highlight_type: HighlightType = HighlightType.UNKNOWN
    evidence: Evidence = Field(default_factory=Evidence)

    @model_validator(mode="after")
    def validate_visual_evidence(self) -> "HairVisualContext":
        # Collect any visual traits that are set to non-UNKNOWN values
        visual_attrs_not_unknown = []
        if self.length.category != HairLengthCategory.UNKNOWN:
            visual_attrs_not_unknown.append("length")
        if self.texture != HairTexture.UNKNOWN:
            visual_attrs_not_unknown.append("texture")
        if self.wave_pattern != WavePattern.UNKNOWN:
            visual_attrs_not_unknown.append("wave_pattern")
        if self.apparent_volume != ApparentVolume.UNKNOWN:
            visual_attrs_not_unknown.append("apparent_volume")
        if self.apparent_density != ApparentDensity.UNKNOWN:
            visual_attrs_not_unknown.append("apparent_density")
        if self.color_family != HairColorFamily.UNKNOWN:
            visual_attrs_not_unknown.append("color_family")
        if self.highlight_type != HighlightType.UNKNOWN:
            visual_attrs_not_unknown.append("highlight_type")

        # If visual attributes are inferred, verify backing evidence exists
        if visual_attrs_not_unknown:
            has_image_evidence = any(
                item.source_type == EvidenceSourceType.IMAGE_OBSERVED
                for item in self.evidence.items
            )
            if not has_image_evidence:
                raise ValueError(
                    f"Visual observations for {', '.join(visual_attrs_not_unknown)} require at least one backing evidence item with source_type IMAGE_OBSERVED."
                )
        return self

class ImageAssessment(BaseModel):
    assessment_id: str = Field(..., description="Unique assessment ID")
    image_ref: ImageReference = Field(..., description="Link to the source image metadata")
    perceived_attributes: HairVisualContext = Field(..., description="The extracted visual facts")
    provenance: Provenance = Field(..., description="Processing node metadata")
