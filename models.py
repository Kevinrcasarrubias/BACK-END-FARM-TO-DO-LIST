from typing import Optional, Any
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic_core import core_schema

# Useful links to solve model and objectId problems:
# https://www.mongodb.com/community/forums/t/pydantic-v2-and-objectid-fields/241965/4
# https://github.com/jefersondaniel/pydantic-mongo/blob/f517e7161a8fb10002ef64881f092f6f84b40971/pydantic_mongo/fields.py
# https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model
# https://stackoverflow.com/questions/76686888/using-bson-objectid-in-pydantic-v2
# https://stackoverflow.com/questions/76686888/using-bson-objectid-in-pydantic-v2/77105412#77105412
# https://stackoverflow.com/questions/76686888/using-bson-objectid-in-pydantic-v2/76837550#76837550
# ⭐ https://www.phind.com/search?cache=k0ftc2onftf3quj0x0pt39aw 🙌🏻


class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)


class Task(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias='_id')
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True
        populate_by_name = True
        json_enconders = {ObjectId: str}


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False

    class Config:
        from_attributes = True
        populate_by_name = True
        json_enconders = {ObjectId: str}