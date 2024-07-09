from marshmallow import Schema,  fields

class ItemModel(Schema):
    name=fields.Str()
    quantity=fields.Int()
    price=fields.Float()
    total=fields.Float(dump_only=True)

class ItemsModel(Schema):
    items=fields.Nested(ItemModel(many=True))
    total=fields.Float(dump_only=True)

class TabModel(Schema):
    id=fields.Str(dump_only=True)
    ibm=fields.Str(required=True)
    tabNumber=fields.Int(required=True)
    createdAt=fields.DateTime(dump_only=True)
    items=fields.Nested(ItemModel(many=True), required=False)
    status=fields.Str(required=False)
    totemId=fields.Str(required=True, load_only=True)

class TabPatch(Schema):
    tabId=fields.Str(required=True)
    item=fields.Nested(ItemModel(many=True))
    
class TabPost(Schema):
    storeId=fields.Str(required=True)
    tabNumber=fields.Int(required=True)

class TabPayment(Schema):
    tabId=fields.Str(required=True)
    cpfOrCnpj=fields.Str()
    email=fields.Str()
    paymentMethod=fields.Str()
    tabs=fields.List(fields.Str(), many=True)
    
class TabConsultPayment(Schema):
    tabId=fields.Str(required=True)
    status=fields.Str(dump_only=True)
    