from typing import Protocol, Optional
from glance.domain.contracts.perception import HairVisualContext
from glance.domain.contracts.intent import HairLookIntent

class HairIntentService(Protocol):
    def classify_intent(
        self, user_input: str, visual_context: Optional[HairVisualContext] = None
    ) -> HairLookIntent:
        """Map natural language prompt input & visual cues to structured look preferences.

        Args:
            user_input: Raw text input from user.
            visual_context: Optional HairVisualContext (visually inferred attributes).

        Returns:
            HairLookIntent representing the user's structured style goals.
        """
        ...
