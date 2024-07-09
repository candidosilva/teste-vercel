from src.services.database import MongoDB

import src.globalvars as globalvars

dev = False
MongoDBConnection = MongoDB( connectionString= globalvars.CONST_MONGO_URL, dataBaseName= globalvars.CONST_DATABASE)
MongoDBConnection.connect(dev)