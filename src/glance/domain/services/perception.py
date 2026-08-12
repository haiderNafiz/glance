from typing import Protocol
from glance.domain.contracts.base import ImageReference
from glance.domain.contracts.perception import ImageAssessment

class HairPerceptionService(Protocol):
    def perceive(self, image: ImageReference) -> ImageAssessment:
        """Analyze an image reference to produce visually inferred observations/attributes.

        Args:
            image: ImageReference containing metadata referencing the input image.

        Returns:
            ImageAssessment containing the structured HairVisualContext and provenance.
        """
        ...
