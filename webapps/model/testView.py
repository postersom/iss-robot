from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model.test import Test
from model.statusView import StatusSchema
from marshmallow import fields


class TestSchema(SQLAlchemyAutoSchema):
    statuses = fields.Nested(StatusSchema, many=True)

    class Meta:
        model = Test


test_schema = TestSchema()
