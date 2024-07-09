import os

os.environ['CONST_MONGO_URL'] = 'mongodb+srv://teste1:testando@cluster0.l1stoef.mongodb.net/?retryWrites=true&w=majority'
os.environ['CONST_DATABASE'] = 'lbc_teste'

os.environ['CONST_STORES_COLLECTION'] = 'stores'
os.environ['CONST_TABS_COLLECTION'] = 'tabs'