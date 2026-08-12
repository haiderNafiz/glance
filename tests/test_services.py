from typing import Optional
from glance.domain.contracts.base import ImageReference, Provenance, Confidence
from glance.domain.contracts.perception import ImageAssessment, HairVisualContext
from glance.domain.contracts.intent import HairLookIntent
from glance.domain.contracts.context import PersonalBeautyContext, BeautyContextUpdate
from glance.domain.contracts.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationCandidate,
    HairLook,
)
from glance.domain.taxonomy.hair import HairLength, HairLengthCategory, LengthLandmark, HaircutStructure
from glance.domain.services.perception import HairPerceptionService
from glance.domain.services.intent import HairIntentService
from glance.domain.services.recommendation import HairLookRecommendationService
from glance.domain.services.context import BeautyContextService

# Implement mock classes adhering to the service Protocols to verify the interfaces
class MockPerceptionService(HairPerceptionService):
    def perceive(self, image: ImageReference) -> ImageAssessment:
        provenance = Provenance(service_name="mock_perception", version="1.0.0", timestamp_utc="2026-08-12T12:00:00Z")
        visual_context = HairVisualContext(image_id=image.image_id)
        return ImageAssessment(
            assessment_id="assess_999",
            image_ref=image,
            perceived_attributes=visual_context,
            provenance=provenance
        )

class MockIntentService(HairIntentService):
    def classify_intent(
        self, user_input: str, visual_context: Optional[HairVisualContext] = None
    ) -> HairLookIntent:
        return HairLookIntent(
            intent_id="intent_999",
            raw_user_prompt=user_input,
            desired_length=HairLengthCategory.MEDIUM
        )

class MockRecommendationService(HairLookRecommendationService):
    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        look = HairLook(
            look_id="look_abc",
            name="Classic Bob",
            length=HairLength(category=HairLengthCategory.SHORT, landmark=LengthLandmark.JAW),
            texture=request.current_intent.desired_texture,
            color=request.current_intent.desired_color,
            haircut_structure=HaircutStructure.BOB,
            description="Classic chin-length cut"
        )
        candidate = RecommendationCandidate(
            candidate_id="cand_abc",
            look=look,
            ranking_score=0.95,
            matching_reasoning="Matches your criteria bob request"
        )
        provenance = Provenance(service_name="mock_recommender", version="1.0.0", timestamp_utc="2026-08-12T12:00:00Z")
        return RecommendationResponse(
            response_id="resp_999",
            request_id=request.request_id,
            candidates=[candidate],
            provenance=provenance
        )

class MockContextService(BeautyContextService):
    def get_context(self, user_id: Optional[str]) -> PersonalBeautyContext:
        return PersonalBeautyContext(user_id=user_id, last_updated="2026-08-12T12:00:00Z")

    def update_context(
        self, context: PersonalBeautyContext, update: BeautyContextUpdate
    ) -> PersonalBeautyContext:
        # Return context back with updated timestamp
        context.last_updated = update.timestamp_utc
        return context

# Test that the stubs implement protocols successfully
def test_perception_service_interface():
    service: HairPerceptionService = MockPerceptionService()
    image = ImageReference(image_id="img_1", url_or_path="http://ref.com/img.jpg", timestamp_utc="2026-08-12T12:00:00Z")
    assessment = service.perceive(image)
    assert assessment.assessment_id == "assess_999"
    assert assessment.image_ref.image_id == "img_1"

def test_intent_service_interface():
    service: HairIntentService = MockIntentService()
    intent = service.classify_intent("I want a medium haircut")
    assert intent.intent_id == "intent_999"
    assert intent.desired_length == HairLengthCategory.MEDIUM

def test_recommendation_service_interface():
    service: HairLookRecommendationService = MockRecommendationService()
    intent = HairLookIntent(intent_id="int_1", raw_user_prompt="I want a bob")
    req = RecommendationRequest(request_id="req_1", current_intent=intent)
    res = service.recommend(req)
    assert res.response_id == "resp_999"
    assert len(res.candidates) == 1
    assert res.candidates[0].look.look_id == "look_abc"

def test_context_service_interface():
    service: BeautyContextService = MockContextService()
    ctx = service.get_context("user_1")
    assert ctx.user_id == "user_1"
    
    update = BeautyContextUpdate(update_id="upd_1", user_id="user_1", timestamp_utc="2026-08-12T13:00:00Z")
    updated_ctx = service.update_context(ctx, update)
    assert updated_ctx.last_updated == "2026-08-12T13:00:00Z"
