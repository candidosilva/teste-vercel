from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from src.functions.tab_functions import creditPaymentMethod, debitPaymentMethod, pixPaymentMethod
from flask_jwt_extended import jwt_required, get_jwt
from src.models.tab_model import TabModel, ItemModel, TabPayment, ItemsModel, TabPatch, TabConsultPayment
from datetime import datetime

blp = Blueprint("Tabs", __name__, description="Acesso as comandas da loja")

def find(arr, elem):
    for x in arr:
       if str(x.get('number')) == elem:
           return x
    else:
        return None 

@blp.route("/tabs")
class TabList(MethodView):
    @blp.response(200, TabModel(many=True))
    def get(self):
        try:
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].find()
            if dbResponse == None:
                abort(404, message="Tabs not found")
            
            tabs = []
            for document in dbResponse:
                tabs.append(document)

            return tabs

        except KeyError:
            abort(500, message="Error getting the tabs.")
            
@blp.route("/tab")
class InsertTab(MethodView):
    @jwt_required()
    @blp.arguments(TabModel)
    @blp.response(201, TabModel)
    def post(self, tab_data):
        try:
            tab = {
                "ibm": tab_data["ibm"],
                "tabNumber": tab_data["tabNumber"],
                "status": "PENDING",
                "createdAt": datetime.now(),
                "totemId": tab_data["totemId"],
                "forma_pagamento": ""
            }
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].insert_one(tab)
            
            response = {
                "id": dbResponse.inserted_id,
                "ibm":  tab_data["ibm"],
                "tabNumber":  tab_data["tabNumber"],
                "createdAt": tab["createdAt"],
                "items": [],
                "status": "PENDING"
            }
            return response
        
        except KeyError:
            abort(500, message="Error creating tab.")
            
@blp.route("/tab/<string:tab_id>")
class TabItens(MethodView):
    @jwt_required()
    @blp.response(200, ItemsModel)
    def get(self, tab_id):
        try:
            filter = {"_id": ObjectId(tab_id)}
            update = {"$set": {"status": "DELIVERED"}}
            tab = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].find_one_and_update(filter, update)
            
            if tab == None:
                abort(404, message="Store not found")

            total = 0
            for item in tab["items"]:
                total = total + item["price"] * item["quantity"]
            
            response = {"items": tab["items"], "total": total}
            return response

        except KeyError:
            abort(500, message="Error getting the store.")

@blp.route("/tab/payment")
class TabPayment(MethodView):
    @jwt_required()
    @blp.arguments(TabPayment)
    def post(self, tab):
        try:
            # jwt = get_jwt()
            # new_payment = {
            #     **tab,
            #     "ibm": jwt["ibm"]
            # }
            filter = {"_id": ObjectId(tab["tabId"])}
            update = {"$set": {"status": "AWAITING", "forma_pagamento": tab["paymentMethod"]}}
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
            if dbResponse.modified_count == 0:
                abort(409, message="Tab not found.")
                
            # if int(new_payment["paymentMethod"]) == 1:
            #     creditPaymentMethod(new_payment)
            # elif int(new_payment["paymentMethod"]) == 2:
            #     debitPaymentMethod(new_payment)
            # else:
            #     pixPaymentMethod(new_payment)
                
            return {"message": "Awaiting payment."}

        except KeyError:
            abort(500, message="Payment Error.")
            
@blp.route("/tab/consult-payment")
class TabConsultPayment(MethodView):
    @jwt_required()
    @blp.arguments(TabConsultPayment)
    @blp.response(200, TabConsultPayment)
    def post(self, tab):
        try:
            filter = {"_id": ObjectId(tab["tabId"])}
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].find_one(filter)
            if dbResponse == None:
                abort(409, message="Tab not found.")
                
            return dbResponse

        except KeyError:
            abort(500, message="Payment Error.")

@blp.route("/tab/cancel")
class TabCancel(MethodView):
    @jwt_required()
    def patch(self, tab):
        try:
            filter = {"_id": ObjectId(tab["tabId"])}
            update = {"$set": {"status": "CANCELED"}}
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
            
            if dbResponse.modified_count == 0:
                abort(409, message="Tab not found.")
                
            return tab["item"]
        
        except KeyError:
            abort(500, message="Error updating tab.")
    
            
# ***********************************************************

# Rota para receber informações de pagamento
# @app.route('/api/inserirPagamento', methods=['POST'])
# def inserirPagamento():
#     data = request.get_json()

#     ibm = data['ibm']
#     id = data['id']
#     valor = data['valor']
#     forma_pagamento = data['forma_pagamento']     
#     numero_serie = data['numero_serie']

#     pagamento_existente = None

#     # Verificar se já existe um pagamento com o mesmo ID e IBM
#     for pagamento in lista_pagamentos:
#         if pagamento['ibm'] == ibm and pagamento['id'] == id and pagamento['numero_serie'] == numero_serie:
#             pagamento_existente = pagamento
#             break

#     if pagamento_existente:
#         # Alterar as informações do pagamento existente
#         pagamento_existente['valor'] = valor
#         pagamento_existente['forma_pagamento'] = forma_pagamento
#     else:
#         # Adicionar o novo pagamento à lista
#         pagamento = {"ibm": ibm, "id": id, "numero_serie": numero_serie, "valor": valor, "forma_pagamento": forma_pagamento, "pago": False}
#         lista_pagamentos.append(pagamento)

#     # Retornar uma resposta de sucesso
#     return {'status': 'success', 'message': 'Informações de pagamento processadas com sucesso'}

# # Rota para obter pagamentos
# @app.route('/api/pagamentos', methods=['GET'])
# def obter_pagamentos_pendentes():
#     return jsonify(lista_pagamentos)

# # Rota para obter pagamento pendente
# @app.route('/api/pagamentoPendente', methods=['GET'])
# def obter_pagamento_pendente():
#     ibm = request.args.get('ibm')
#     numero_serie = request.args.get('numero_serie')
    
#     if ibm is not None:
#         try:
#             ibm = int(ibm)  # Converter para inteiro
#         except ValueError:
#             return jsonify({"error": "IBM inválido"}), 400
#     else:
#         return jsonify({"error": "IBM obrigatório"}), 400
    
#     return jsonify(retornar_proximo_pagamento_pendente(ibm, numero_serie, lista_pagamentos))

# def retornar_proximo_pagamento_pendente(ibm, numero_serie, pagamentos):
#     for pagamento in pagamentos:
#         if ((not pagamento["pago"]) & (pagamento["ibm"] == ibm) & (pagamento["numero_serie"] == numero_serie)):
#             return pagamento

#     return {"id": -1}

# # Rota para atualizar pagamento
# @app.route('/api/atualizarPagamento', methods=['PUT'])
# def atualizar_pagamento():
#     data = request.get_json()

#     ibm = data["ibm"]
#     id = data['id']
#     pago = data ['pago']
#     numero_serie = data ['numero_serie']

#     for pagamento in lista_pagamentos:
#         if ((pagamento["ibm"] == ibm) & (pagamento["id"] == id) & (pagamento["numero_serie"] == numero_serie)):
#             pagamento['pago'] = pago
#             return {'status': 'success', 'message': 'Pagamento atualizado com sucesso'}

#     return {'status': 'error', 'message': 'Pagamento não encontrado'}
