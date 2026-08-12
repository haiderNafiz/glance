from typing import Protocol, Optional
from glance.domain.contracts.context import PersonalBeautyContext, BeautyContextUpdate

class BeautyContextService(Protocol):
    def get_context(self, user_id: Optional[str]) -> PersonalBeautyContext:
        """Retrieve stable preference context for a specific user ID.

        If user_id is None, returns an empty/cold-start context snapshot.

        Args:
            user_id: Optional string identifying the user.

        Returns:
            PersonalBeautyContext populated with stable learned preferences.
        """
        ...

    def update_context(
        self, context: PersonalBeautyContext, update: BeautyContextUpdate
    ) -> PersonalBeautyContext:
        """Apply a preference delta update payload to update the stable context.

        Args:
            context: Current PersonalBeautyContext profile.
            update: BeautyContextUpdate package.

        Returns:
            PersonalBeautyContext containing updated preferences.
        """
        ...
