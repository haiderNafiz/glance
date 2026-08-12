from typing import Protocol
from glance.domain.contracts.recommendation import RecommendationRequest, RecommendationResponse

class HairLookRecommendationService(Protocol):
    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        """Evaluate visual & intent context along with stable preferences to suggest matching hair looks.

        Args:
            request: RecommendationRequest detailing current user query constraints.

        Returns:
            RecommendationResponse containing product-independent recommended looks.
        """
        ...
