from pydantic import BaseModel, constr


class MainBehaviourCompositionOutput(BaseModel):
    main_behaviour: constr(max_length=100)
