import pytest
from pydantic import ValidationError
from glance.domain.taxonomy.hair import (
    HairLengthCategory,
    LengthLandmark,
    HairLength,
    HairTexture,
    WavePattern,
    ApparentVolume,
    ApparentDensity,
    HairColorFamily,
    HighlightType,
    HaircutStructure,
)

def test_taxonomy_enums():
    # Verify categories match expectation
    assert HairLengthCategory.VERY_SHORT == "VERY_SHORT"
    assert HairLengthCategory.LONG == "LONG"
    assert LengthLandmark.SCALP_CLOSE == "SCALP_CLOSE"
    assert HairTexture.WAVY == "WAVY"
    assert WavePattern.DEFINED == "DEFINED"
    assert ApparentVolume.HIGH == "HIGH"
    assert ApparentDensity.LOW == "LOW"
    assert HairColorFamily.DARK_BROWN == "DARK_BROWN"
    assert HighlightType.MULTI_TONE == "MULTI_TONE"
    assert HaircutStructure.LAYERED == "LAYERED"

def test_hair_length_validation():
    # Valid model with categories
    hl = HairLength(
        category=HairLengthCategory.SHOULDER_LENGTH,
        landmark=LengthLandmark.SHOULDER,
        estimated_cm=35.5
    )
    assert hl.category == HairLengthCategory.SHOULDER_LENGTH
    assert hl.estimated_cm == 35.5

    # Default values
    hl_default = HairLength()
    assert hl_default.category == HairLengthCategory.UNKNOWN
    assert hl_default.landmark == LengthLandmark.UNKNOWN
    assert hl_default.estimated_cm is None

    # Invalid estimated_cm (negative)
    with pytest.raises(ValidationError):
        HairLength(estimated_cm=-5.0)
