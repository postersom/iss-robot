from marshmallow_sqlalchemy import ModelSchema
from model.test import Test
from model.status import Status
from model.statusView import StatusSchema
from marshmallow import fields


class TestSchema(ModelSchema):
    statuses = fields.Nested(StatusSchema, many=True)

    class Meta:
        model = Test


test_schema = TestSchema()
