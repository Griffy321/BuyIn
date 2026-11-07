from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

# contracts for requests that come in
class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

class CreatePlayerRequest(CamelModel):
    first_name: str
    last_name: str

