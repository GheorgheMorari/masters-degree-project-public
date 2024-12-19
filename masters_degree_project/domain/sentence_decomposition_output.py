from typing import Annotated, List

from annotated_types import Len
from pydantic import BaseModel, StringConstraints

class EntityModifiersPair(BaseModel):
    entity: Annotated[str, StringConstraints(max_length=100)]
    entity_modifiers: Annotated[List[Annotated[str, StringConstraints(max_length=100)]], Len(min_length=1, max_length=10)]

class BehaviorModifiersPair(BaseModel):
    behavior: Annotated[str, StringConstraints(max_length=100)]
    behavior_modifiers: Annotated[List[Annotated[str, StringConstraints(max_length=100)]], Len(min_length=1, max_length=10)]

class SentenceDecompositionOutput(BaseModel):
    entity_modifier_pairs: Annotated[List[EntityModifiersPair], Len(min_length=1, max_length=10)]
    behavior_modifier_pairs: Annotated[List[BehaviorModifiersPair], Len(min_length=1, max_length=10)]
    main_clause: Annotated[str, StringConstraints(max_length=200)]
