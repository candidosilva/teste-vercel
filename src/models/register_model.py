from marshmallow import Schema, fields

class RegisterModel(Schema):
    totemId=fields.Str(required=True)  
    token=fields.Str(dump_only=True)
    