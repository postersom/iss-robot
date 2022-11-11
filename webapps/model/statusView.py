# from marshmallow_sqlalchemy import ModelSchema
# from model.status import Status
#
#
# class StatusSchema(ModelSchema):
#     class Meta:
#         model = Status
#         ordered = True
#
# status_schema = StatusSchema()


from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model.status import Status


class StatusSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Status
        ordered = True


status_schema = StatusSchema()
