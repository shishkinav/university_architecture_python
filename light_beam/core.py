from typing import Dict, List, Callable
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from views import PageNotFound404


class LightBeamApp:
    def __init__(self, routes: Dict, controllers: List) -> None:
        self.routes: dict = routes
        self.controllers: list = controllers

    def __call__(self, environ: Dict, start_response: Callable):
        setup_testing_defaults(environ)
        path = environ.get('PATH_INFO')
        # Проверка вхождения запрошенного пути в список наших роутеров
        if path in self.routes.keys():
            _view = self.routes[path]
        else:
            _view = PageNotFound404()
        request = dict()
        for controller in self.controllers:
            controller(request)
        code, body = _view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]




