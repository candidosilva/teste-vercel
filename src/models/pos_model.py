from marshmallow import Schema,  fields

class POSModel(Schema):
    storeId=fields.Str(required=True)
    totemId=fields.Str(required=True)
    pos=fields.Str(required=True)
    
class AtualizarPagamentoModel(Schema):
    ibm=fields.Str(required=True, load_only=True)
    numero_serie=fields.Str(required=True, load_only=True)
    status=fields.Str(dump_only=True)