from glance.domain.contracts.base import (
    Confidence,
    EvidenceSourceType,
    EvidenceItem,
    Evidence,
    Provenance,
    ImageReference,
)
from glance.domain.contracts.perception import (
    HairVisualContext,
    ImageAssessment,
)
from glance.domain.contracts.intent import (
    HairLookIntent,
)
from glance.domain.contracts.context import (
    LearnedHairPreference,
    PersonalBeautyContext,
    BeautyContextUpdate,
)
from glance.domain.contracts.recommendation import (
    HairLook,
    RecommendationRequest,
    RecommendationCandidate,
    RecommendationResponse,
    BeautyFeedback,
)
from glance.domain.contracts.knowledge import (
    BeautyKnowledgeReference,
)
