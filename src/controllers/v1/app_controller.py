from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson.objectid import ObjectId
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from src.functions.tab_functions import creditPaymentMethod, debitPaymentMethod, pixPaymentMethod
from flask_jwt_extended import jwt_required, get_jwt
from src.models.tab_model import TabModel, ItemModel, TabPayment, ItemsModel, TabPatch, TabConsultPayment
from datetime import datetime

blp = Blueprint("App", __name__, description="Controller do app")

@blp.route("/tab/app/<string:ibm>")
class TabList(MethodView):
    @blp.response(200, TabModel(many=True))
    def get(self, ibm):
        try:
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].find({"ibm": ibm, "status": "PENDING"})
            tabs = []
            
            if dbResponse == None:
                return tabs
            
            for document in dbResponse:
                tabs.append(document)

            return tabs

        except KeyError:
            abort(500, message="Error getting the tabs.")
            
@blp.route("/tab/app")
class UpdateTab(MethodView):
    @blp.arguments(TabPatch)
    @blp.response(200, ItemModel)
    def patch(self, tab_data):
        try:
            filter = {"_id": ObjectId(tab_data["tabId"])}
            update = {"$push": {"items": tab_data["item"]}, "$set": {"status": "DELIVERED"}}
            dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
            
            if dbResponse.modified_count == 0:
                abort(409, message="Tab not found.")
                
            return tab_data["item"]
        
        except KeyError:
            abort(500, message="Error updating tab.")