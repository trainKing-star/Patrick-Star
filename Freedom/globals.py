from functools import partial
#partial设置函数默认值，返回一个新函数
from werkzeug.local import LocalProxy,LocalStack

request_error = 'no request context'
app_error = 'no app context'

def search_request(name):
    top = request_stack.top
    if top is None:
        raise RuntimeError(request_error)
    return getattr(top,name)
#getattr根据字符串返回方法

def search_app(name):
    top = app_stack.top
    if top is None:
        raise RuntimeError(app_error)
    return getattr(top,name)

def find_app():
    top = app_stack.top
    if top is None:
        raise  RuntimeError(app_error)
    return top.app

request_stack = LocalStack()
app_stack = LocalStack()

current_app = LocalProxy(find_app)
request = LocalProxy(partial(search_request,'request'))
session = LocalProxy(partial(search_request,'session'))
g = LocalProxy(partial(search_app,'g'))