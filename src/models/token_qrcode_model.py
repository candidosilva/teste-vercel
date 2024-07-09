from marshmallow import Schema,  fields

class TokenModel(Schema):
    ibm=fields.Str(required=True, load_only=True)
    id=fields.Str(required=True, load_only=True)
    token=fields.Str(dump_only=True)