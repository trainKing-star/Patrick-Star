
from werkzeug.wrappers import Request,Response
from werkzeug.exceptions import HTTPException
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from globals import request_stack,app_stack

secret_key = 'secret_key'

class RequestContext:
    def __init__(self,app,environ):
        self.app = app
        self.request = Request(environ)
        self.url_adapter = app.url_map.bind_to_environ(self.request.environ)
        self.session = {}

    def create_session(self):
        s = Serializer(secret_key)
        token = self.app.search_session()
        if token is not None:
            self.session = s.loads(token)


    def set_token(self):
        s = Serializer(secret_key,expires_in=6000)
        if self.session:
            return (s.dumps(self.session)).decode('utf-8')
        return None

    def match_request(self):
        result = self.url_adapter.match()
        return result

    def push(self):
        top = request_stack.top
        if top is not None:
            request_stack.pop()
        top =app_stack.top
        if top is None or top.app != self.app:
            app_x = AppContext(self.app,self.request.environ)
            app_x.push()
        request_stack.push(self)
        self.create_session()


    def pop(self):
        top = request_stack.top
        if top is not None:
            request_stack.pop()

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        request_stack.pop(self)


_sentinel = object()


class AppGlobals:
    pass


class AppContext:
    def __init__(self,app,environ):
        self.app = app
        #self.request = Request(environ)
        self.url_adapter = app.url_map.bind_to_environ(environ)
        self.g = AppGlobals

    def push(self):
        top = app_stack.top
        if top is not None:
            app_stack.pop()
        app_stack.push(self)

    def pop(self):
        top = app_stack.top
        if top is not None:
            app_stack.pop()
