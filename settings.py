NODE_URL = 'http://node2.storj.io'
SECRET_KEY = 'i-am-a-super-secret-dev-key'

try:
    from local_settings import *
except ImportError:
    pass