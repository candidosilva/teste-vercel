from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from src.models.register_model import RegisterModel
from src.models.store_model import StorePost

blp = Blueprint("Register", __name__, description="Registro do totem na loja")

@blp.route("/register")
class Register(MethodView):
    @jwt_required()
    @blp.arguments(RegisterModel)
    @blp.response(200, StorePost)
    def post(self, store_data):
        try:   
            jwt = get_jwt()
            totem = {
                "id": store_data["totemId"], 
                "pos": "Sem POS cadastrado",
                "token": create_access_token(identity=jwt["ibm"], additional_claims={"id": jwt["sub"]}, expires_delta=False)
            }
            store = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one_and_update({"_id": ObjectId(jwt["sub"])}, {"$push": {"totems": totem}})
            if store == None:
                abort(404, message="Store not found")
            
            if hasattr(store, 'totems'):
                store["totems"].append(totem)
            else:
                store["totems"] = []
                store["totems"].append(totem)
                
            return store
        
        except KeyError:
            abort(500, message="Error getting the store.")