from marshmallow import Schema,  fields

class ItensModel(Schema):
    name=fields.Str()
    quantity=fields.Int()
    price=fields.Float()
    
class TabsModel(Schema): 
    number=fields.Int(required=True)
    itens=fields.Nested(ItensModel(many=True))
    paying=fields.Str()
    
class TotemModel(Schema):
    id=fields.Str(dump_only=True)
    pos=fields.Str()
    token=fields.Str()
    
class StoreModel(Schema):
    id=fields.Str(dump_only=True)
    ibm=fields.Str(required=True)
    cnpj=fields.Str(required=True)
    name=fields.Str(required=True)
    logoUrl=fields.Str(required=True)
    totems=fields.Nested(TotemModel(many=True), required=False, dump_only=True)
    createdAt=fields.DateTime(dump_only=True)
    
class StorePost(Schema):
    id=fields.Str(dump_only=True)
    name=fields.Str(required=True)
    logoUrl=fields.Str(required=True)
    totems=fields.List(fields.Str(), many=True, required=False)
    tabs=fields.Nested(TabsModel(many=True))