from typing import Annotated

from pydantic import BaseModel, StringConstraints


class MainBehaviourCompositionOutput(BaseModel):
    main_behaviour: Annotated[str, StringConstraints(max_length=100)]
