from marshmallow_sqlalchemy import ModelSchema
from model.status import Status


class StatusSchema(ModelSchema):
    class Meta:
        model = Status
        ordered = True
        # optionally attach a Session
        # to use for deserialization


status_schema = StatusSchema()
