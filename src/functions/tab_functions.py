import time
from src.services.__init__ import MongoDBConnection
import src.globalvars as globalvars
from bson.objectid import ObjectId
from flask_smorest import abort

def setTimeout(timeout=5):
    start_time = time.time()
    for _ in range(10):
        if time.time()-start_time > timeout:
           break
        time.sleep(1)

def creditPaymentMethod(tab):
    setTimeout()    
    filter = {"_id": ObjectId(tab["tabId"])}
    update = {"$set": {"status": "COMPLETED", "items": []}}
    dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
    
    if dbResponse.modified_count == 0:
        abort(409, message="Tab not updated.")
        
    return True

def debitPaymentMethod(tab):
    setTimeout()
    filter = {"_id": ObjectId(tab["tabId"])}
    update = {"$set": {"status": "COMPLETED", "items": []}}
    dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
    
    if dbResponse.modified_count == 0:
        abort(409, message="Tab not updated.")
        
    return True

def pixPaymentMethod(tab):
    setTimeout()
    filter = {"_id": ObjectId(tab["tabId"])}
    update = {"$set": {"status": "COMPLETED", "items": []}}
    dbResponse = MongoDBConnection.dataBase()[globalvars.CONST_TABS_COLLECTION].update_one(filter, update)
    
    if dbResponse.modified_count == 0:
        abort(409, message="Tab not updated.")
        
    return True