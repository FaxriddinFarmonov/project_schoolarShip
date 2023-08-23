from api import v1
from methodism import METHODISM

class Main(METHODISM):
    file = v1
    not_auth_methods = ['*']