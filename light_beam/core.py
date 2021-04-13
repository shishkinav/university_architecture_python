from typing import Dict, List, Callable
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


class LightBeamApp:
    def __init__(self, routes: Dict, controllers: List) -> None:
        self.routes: dict = routes
        self.controllers: list = controllers

    def __call__(self, environ: Dict, start_response: Callable):
        setup_testing_defaults(environ)
        # сначала в функцию start_response передаем код ответа и заголовки
        start_response('200 OK', [('Content-Type', 'text/html')])
        # возвращаем тело ответа в виде списка из bite
        return [b'<h1>Hello my simple WSGI application!</h1>']




