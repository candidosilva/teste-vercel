import os

try:
    import src.secret
except:
    pass

'''DATABASE'''
CONST_MONGO_URL = os.environ.get('CONST_MONGO_URL')
CONST_DATABASE = os.environ.get('CONST_DATABASE')

'''COLLECTIONS'''
CONST_STORES_COLLECTION = os.environ.get('CONST_STORES_COLLECTION')
CONST_TABS_COLLECTION = os.environ.get('CONST_TABS_COLLECTION')

'''Caches'''
CACHE_MEMBERS_MAX_SIZE = 200
CONST_CACHE_EXPIRATION = 60 * 60 * 8 # 8 hours

'''GENERAL'''
TOKEN_SECRET = os.environ.get('TOKEN_SECRET')