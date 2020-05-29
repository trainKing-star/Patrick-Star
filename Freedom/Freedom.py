
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from werkzeug.routing import Map,Rule
from werkzeug.utils import redirect
from werkzeug.wsgi import SharedDataMiddleware
from jinja2 import Environment,FileSystemLoader
from werkzeug.exceptions import HTTPException
from ctx import RequestContext
from globals import request_stack,app_stack
import functools
import redis
import os


class Freedom(object):
    def __init__(self):
        self.template='templates'
        template_path = os.path.join(os.path.dirname(__file__), self.template)
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        self.url_map=Map()
        self.app_path=None
        self.view_functions = {}
        self.set_static()

    def set_static(self,static='static',static_path='/static'):
        self.url_map.add(Rule(static_path+'/<filename>',build_only=True,endpoint='static'))
        self.app_path =  os.path.join(os.path.dirname(__file__), static)
        self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
            static_path: self.app_path
        })

    def set_templates(self,template=None):
        if template:
            self.template=template
            template_path = os.path.join(os.path.dirname(__file__),self.template)
            self.jinja_env=Environment(loader=FileSystemLoader(template_path),autoescape=True)

    def drawing_template(self,template_name,**context):
        data =self.jinja_env.get_template(template_name)
        return Response(data.render(context),mimetype='text/html')

    def register_url(self,rule,endpoint,view_func,methods):
        rule = Rule(rule,endpoint=endpoint,methods=methods)
        self.url_map.add(rule)
        self.view_functions[endpoint]=view_func

    def way(self,rule,methods=None):
        if methods == None:
            methods = ['GET']
        def decorator(func):
            self.register_url(rule, func.__name__, func,methods)
            #@functools.wraps(func)
            '''def wrapper(*args,**kwargs):
                self.register_url(rule,func.__name__,func)
                return func'''
            return func
        return decorator


    def make_response(self,re):
        if isinstance(re,Response):
            return re
        elif isinstance(re,bytes):
            return re
        elif re is None:
            raise TypeError('no return')
        else:
            return Response(re)

    def search_session(self):
        request = request_stack.top
        if request.request.cookies.get('session') is not None:
            return request.request.cookies.get('session')
        return None


    def dispatch_request(self,response):
        request = request_stack.top
        try:
            endpoint, values = request.match_request()
            re = self.view_functions[endpoint](**values)
            response = self.make_response(re)
            session = request.set_token()
            if session is not None:
                response.set_cookie('session', session)
            else:
                response.delete_cookie('session')
            return response
        except HTTPException:
            return Response('not fond')


    def wsgi_app(self,environ,start_response):
        cc = RequestContext(self,environ)
        try:
            cc.push()
            response = Response(environ)
            response = self.dispatch_request(response)
            return response(environ, start_response)
        finally:
            cc.pop()

    def __call__(self,environ,start_response):
        return self.wsgi_app(environ,start_response)

    def fly(self,host=None,port=None,debug=None):
        if not host:
            host='127.0.0.1'
        if not port:
            port=5000
        run_simple(host,port,self,use_debugger=debug,use_evalex=True,use_reloader=True)
