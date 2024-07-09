from pprint import pprint
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from flask_jwt_extended import jwt_required
from flask import request
import hashlib

from src.models.pos_model import POSModel, AtualizarPagamentoModel

blp = Blueprint("POS", __name__, description="Registro do POS na loja")

@blp.route("/pos")
class POS(MethodView):
    @jwt_required()
    @blp.arguments(POSModel)
    @blp.response(200, POSModel)
    def patch(self, pos_data):
        try:   
            filter = {"_id": ObjectId(pos_data["storeId"]), "totems.id": pos_data["totemId"]}
            update = {"$set": {"totems.$.pos": pos_data["pos"]}}
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].update_one(filter, update)
            
            if dbResponse.modified_count == 0:
                abort(409, message="Tab not updated.")
                
            return pos_data
        
        except KeyError:
            abort(500, message="Error getting the store.")
            
@blp.route("/pos/pagamentoPendente/<string:ibm>/<string:numero_serie>")
class TabPending(MethodView):
    @blp.response(200)
    def patch(self, ibm, numero_serie):
        try:   
            authorization = request.headers.get('Authorization')
            hash = hashlib.md5(f"TOTEM LBC IBM:{ibm} SERIAL:{numero_serie }".encode()).hexdigest()
            print(hash)
            print(authorization)
            if authorization == hash:
                filter = {"ibm": ibm, "totems": {"$elemMatch": {"pos": numero_serie}}}
                store = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one(filter)
                
                totemId = None
                if store:
                    for totem in store["totems"]:
                        if totem["pos"] == numero_serie:
                            totemId = totem["id"]
                            break
                else:
                    abort(401, message="Store not found")
                filter = {"ibm": ibm, "totemId": totemId, "status": "AWAITING"}
                tab = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].find_one(filter)
                
                total = 0
                for item in tab["items"]:
                    total = total + item["price"] * item["quantity"]
                    
                if tab:
                    return {
                        "forma_pagamento": tab["forma_pagamento"],
                        "ibm": tab["ibm"],
                        "id": tab["tabNumber"],
                        "numero_serie": numero_serie,
                        "pago": False,
                        "valor": total
                    }
                else:
                    return {"id": -1}
            else:
                abort(401, message="Not authorized")
                
        except KeyError:
            abort(500, message="Error getting the store.")
            
@blp.route("/pos/atualizarPagamento")
class AtualizarPagamento(MethodView):
    @blp.arguments(AtualizarPagamentoModel)
    @blp.response(200, AtualizarPagamentoModel)
    def patch(self, data):
        try:
            authorization = request.headers.get('Authorization')
            hash = hashlib.md5(f"TOTEM LBC IBM:{data["ibm"]} SERIAL:{data["numero_serie"]}".encode()).hexdigest()
            if authorization == hash:
                filter = {"ibm": data["ibm"], "totems": {"$elemMatch": {"pos": data['numero_serie']}}}
                store = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one(filter)
                
                totemId = None
                if store:
                    for totem in store["totems"]:
                        if totem["pos"] == data['numero_serie']:
                            totemId = totem["id"]
                            break
                else:
                    abort(401, message="Store not found")
                    
                filter = {"ibm": data["ibm"], "totemId": totemId, "status": "AWAITING" }
                update = {"$set": {"status": "COMPLETED"}}
                tab = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
                
                if tab.modified_count == 0:
                    abort(409, message="Tab not updated.")
            
                return {"status": "COMPLETED"}
            else:
                abort(401, message="Not authorized")
                
        except KeyError:
            abort(500, message="Error getting the store.")