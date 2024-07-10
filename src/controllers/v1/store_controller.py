from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from datetime import datetime

from src.models.store_model import StoreModel

blp = Blueprint("Stores", __name__, description="Acesso as stores")

@blp.route("/store")
class Store(MethodView):
    @blp.arguments(StoreModel)
    @blp.response(201, StoreModel)
    def post(self, store_data):
        try:
            new_store = {**store_data}
            new_store["ibm"] = new_store["ibm"].zfill(14)
            new_store["createdAt"] = datetime.now()
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].insert_one(new_store)
            store_response = {**new_store, "id": dbResponse.inserted_id, "totems": []}
            return store_response
        
        except KeyError:
            abort(500, message="Error creating store.")

@blp.route("/store/<string:store_id>")
class StoreList(MethodView):
    @blp.response(200, StoreModel)
    def get(self, store_id):
        try:
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find_one({"_id": ObjectId(store_id)})
            
            if dbResponse == None:
                abort(404, message="Store not found")

            return dbResponse

        except KeyError:
            abort(500, message="Error getting the store.")
            
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreModel(many=True))
    def get(self):
        try:
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_STORES_COLLECTION].find()
            
            if dbResponse == None:
                abort(404, message="Stores not found")
            
            stores = []
            for document in dbResponse:
                stores.append({**document, "id": document["_id"]})

            return stores

        except KeyError:
            abort(500, message="Error getting the store.")