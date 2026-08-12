import pytest
from pydantic import ValidationError
from glance.domain.contracts.base import (
    Confidence,
    EvidenceSourceType,
    EvidenceItem,
    Evidence,
    Provenance,
    ImageReference,
)
from glance.domain.contracts.perception import HairVisualContext, ImageAssessment
from glance.domain.contracts.intent import HairLookIntent
from glance.domain.contracts.context import LearnedHairPreference, PersonalBeautyContext
from glance.domain.contracts.recommendation import (
    HairLook,
    RecommendationRequest,
    RecommendationCandidate,
    RecommendationResponse,
    BeautyFeedback,
)
from glance.domain.taxonomy.hair import (
    HairLength,
    HairLengthCategory,
    LengthLandmark,
    HairTexture,
    WavePattern,
    ApparentVolume,
    ApparentDensity,
    HairColorFamily,
    HighlightType,
    HaircutStructure,
)

# 1. Confidence validation tests
def test_confidence_validation():
    # Valid
    c = Confidence(score=0.85)
    assert c.score == 0.85

    # Valid boundaries
    Confidence(score=0.0)
    Confidence(score=1.0)

    # Invalid values
    with pytest.raises(ValidationError):
        Confidence(score=-0.1)
    with pytest.raises(ValidationError):
        Confidence(score=1.01)


# 2. ImageReference validation tests
def test_image_reference_validation():
    # Valid URL
    ref = ImageReference(image_id="img_123", url_or_path="http://example.com/hair.jpg", timestamp_utc="2026-08-12T12:00:00Z")
    assert ref.image_id == "img_123"

    # Valid Path
    ref_path = ImageReference(image_id="img_123", url_or_path="/local/path/to/hair.png", timestamp_utc="2026-08-12T12:00:00Z")
    assert ref_path.url_or_path == "/local/path/to/hair.png"

    # Invalid: base64 data uri
    with pytest.raises(ValidationError):
        ImageReference(
            image_id="img_123",
            url_or_path="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA",
            timestamp_utc="2026-08-12T12:00:00Z",
        )

    # Invalid: raw base64 string
    with pytest.raises(ValidationError):
        ImageReference(
            image_id="img_123",
            url_or_path="aGVsbG93b3JsZAaGVsbG93b3JsZAaGVsbG93b3JsZAaGVsbG93b3JsZAaGVsbG93b3JsZAaGVsbG93b3JsZAaGVsbG93b3JsZA",
            timestamp_utc="2026-08-12T12:00:00Z",
        )


# 3. EvidenceItem bounding box validation tests
def test_evidence_item_bounding_box():
    confidence = Confidence(score=0.9)
    # Valid bounding box
    item = EvidenceItem(
        source_type=EvidenceSourceType.IMAGE_OBSERVED,
        bounding_box=[10.0, 20.0, 50.0, 60.0],
        description="Visible highlights in visual region",
        confidence=confidence,
    )
    assert item.bounding_box == [10.0, 20.0, 50.0, 60.0]

    # Invalid coordinates size
    with pytest.raises(ValidationError):
        EvidenceItem(
            source_type=EvidenceSourceType.IMAGE_OBSERVED,
            bounding_box=[10.0, 20.0, 30.0],
            description="Invalid length",
            confidence=confidence,
        )

    # Invalid negative values
    with pytest.raises(ValidationError):
        EvidenceItem(
            source_type=EvidenceSourceType.IMAGE_OBSERVED,
            bounding_box=[-1.0, 2.0, 3.0, 4.0],
            description="Negative coord",
            confidence=confidence,
        )


# 4. HairVisualContext evidence validation tests
def test_hair_visual_context_validation():
    # If all attributes are UNKNOWN, no evidence is required
    context_unknown = HairVisualContext(image_id="img_123")
    assert context_unknown.length.category == HairLengthCategory.UNKNOWN
    assert len(context_unknown.evidence.items) == 0

    # If any attribute is not UNKNOWN, image evidence MUST be provided
    with pytest.raises(ValidationError):
        HairVisualContext(
            image_id="img_123",
            texture=HairTexture.WAVY,
            evidence=Evidence(items=[]) # Missing evidence
        )

    # Invalid: Evidence present but NOT IMAGE_OBSERVED
    confidence = Confidence(score=0.9)
    with pytest.raises(ValidationError):
        HairVisualContext(
            image_id="img_123",
            texture=HairTexture.WAVY,
            evidence=Evidence(
                items=[
                    EvidenceItem(
                        source_type=EvidenceSourceType.USER_DECLARED, # Incorrect source type
                        description="User said they have wavy hair",
                        confidence=confidence
                    )
                ]
            )
        )

    # Valid: Non-UNKNOWN visual context with IMAGE_OBSERVED evidence
    context_valid = HairVisualContext(
        image_id="img_123",
        texture=HairTexture.WAVY,
        evidence=Evidence(
            items=[
                EvidenceItem(
                    source_type=EvidenceSourceType.IMAGE_OBSERVED,
                    description="Detected wavy pattern in visual zone",
                    confidence=confidence
                )
            ]
        )
    )
    assert context_valid.texture == HairTexture.WAVY


# 5. Intent contract does NOT require image evidence
def test_hair_look_intent_evidence():
    # Intent with USER_DECLARED evidence and no IMAGE_OBSERVED
    confidence = Confidence(score=1.0)
    intent = HairLookIntent(
        intent_id="int_001",
        raw_user_prompt="I want a blonde bob",
        desired_length=HairLengthCategory.SHORT,
        desired_color=HairColorFamily.BLONDE,
        evidence=Evidence(
            items=[
                EvidenceItem(
                    source_type=EvidenceSourceType.USER_DECLARED,
                    description="User prompt declaration",
                    confidence=confidence
                )
            ]
        )
    )
    assert intent.desired_color == HairColorFamily.BLONDE
    # Should validate cleanly without throwing errors


# 6. PersonalBeautyContext cold start tests
def test_personal_beauty_context_cold_start():
    # Genuinely cold-start valid: completely empty preferences
    context_cold = PersonalBeautyContext(
        user_id=None,
        last_updated="2026-08-12T12:00:00Z"
    )
    assert context_cold.user_id is None
    assert len(context_cold.learned_preferences.preferred_lengths) == 0
    assert context_cold.learned_preferences.confidence is None
    assert context_cold.learned_preferences.last_evaluated is None

    # Fully populated preferences
    confidence = Confidence(score=0.95)
    context_populated = PersonalBeautyContext(
        user_id="user_123",
        learned_preferences=LearnedHairPreference(
            preferred_lengths=[HairLengthCategory.MEDIUM],
            confidence=confidence,
            last_evaluated="2026-08-12T12:00:00Z"
        ),
        last_updated="2026-08-12T12:00:00Z"
    )
    assert context_populated.learned_preferences.confidence.score == 0.95


# 7. RecommendationResponse candidate count validation tests
def test_recommendation_response_candidate_validation():
    look = HairLook(
        look_id="look_1",
        name="Layered Cut",
        length=HairLength(category=HairLengthCategory.MEDIUM, landmark=LengthLandmark.SHOULDER),
        texture=HairTexture.WAVY,
        color=HairColorFamily.DARK_BROWN,
        haircut_structure=HaircutStructure.LAYERED,
        description="A nice layered medium length cut"
    )
    candidate = RecommendationCandidate(
        candidate_id="cand_1",
        look=look,
        ranking_score=0.9,
        matching_reasoning="Fits your preferred color and style tags"
    )
    provenance = Provenance(
        service_name="recommender",
        version="1.0.0",
        timestamp_utc="2026-08-12T12:00:00Z"
    )

    # Valid: 1 candidate
    resp_valid = RecommendationResponse(
        response_id="resp_123",
        request_id="req_123",
        candidates=[candidate],
        provenance=provenance
    )
    assert len(resp_valid.candidates) == 1

    # Invalid: 0 candidates
    with pytest.raises(ValidationError):
        RecommendationResponse(
            response_id="resp_123",
            request_id="req_123",
            candidates=[],
            provenance=provenance
        )

    # Invalid: 6 candidates
    with pytest.raises(ValidationError):
        RecommendationResponse(
            response_id="resp_123",
            request_id="req_123",
            candidates=[candidate] * 6,
            provenance=provenance
        )


# 8. BeautyFeedback bounds validation
def test_beauty_feedback_validation():
    # Valid
    BeautyFeedback(
        feedback_id="fb_123",
        look_id="look_1",
        response_id="resp_1",
        rating=4,
        timestamp_utc="2026-08-12T12:00:00Z"
    )

    # Rating boundary failures
    with pytest.raises(ValidationError):
        BeautyFeedback(
            feedback_id="fb_123",
            look_id="look_1",
            response_id="resp_1",
            rating=0, # Below 1
            timestamp_utc="2026-08-12T12:00:00Z"
        )
    with pytest.raises(ValidationError):
        BeautyFeedback(
            feedback_id="fb_123",
            look_id="look_1",
            response_id="resp_1",
            rating=6, # Above 5
            timestamp_utc="2026-08-12T12:00:00Z"
        )
