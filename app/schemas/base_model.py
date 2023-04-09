from humps import camel
from pydantic import BaseModel


class AppBaseModelConfig:
    alias_generator = camel.case
    allow_population_by_field_name = True
    orm_mode = True


# Handle camelCase + ORM mode
class AppBaseModel(BaseModel):
    class Config(AppBaseModelConfig):
        pass
