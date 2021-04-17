from typing import Dict, List, Callable
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from views import PageNotFound404
import quopri
import logging


logger = logging.getLogger(__name__)


class LightBeamApp:
    def __init__(self, routes: Dict, controllers: List) -> None:
        self.routes: dict = routes
        self.controllers: list = controllers

    def get_request_data(self, env: dict) -> dict:
        """Метод обработки данных полученного запроса и возврат
            данных для обновления нашего request"""
        method = env['REQUEST_METHOD']
        _data: dict = (self.get_query_param(env),
                       self.post_params(env))[method == "POST"]
        _data.update({"method": method})
        return _data

    def decode_value(self, data: dict) -> dict:
        """Декодирование кириллических символов"""
        def convert_str(value):
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            return quopri.decodestring(val).decode('UTF-8')

        return {convert_str(key): convert_str(value) \
            for key, value in data.items()}

    def parse_data(self, data: str) -> dict:
        """Преобразование string в dict"""
        try:
            if data:
                params = data.split('&')
                res = [item.split('=') for item in params]
                return self.decode_value({key: value for key, value in res})
            else:
                return {}
        except:
            return {}

    def get_query_param(self, env: dict) -> dict:
        """Извлечение параметров запроса GET"""
        query_string: str = env['QUERY_STRING']
        return {'GET_params': self.parse_data(query_string)}

    def post_params(self, env: dict) -> dict:
        """Извлечение параметров запроса POST"""
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(
            content_length) if content_length > 0 else b''
        data_str = data.decode(encoding='utf-8') if data else ''
        return {'POST_params': self.parse_data(data_str)}
        
    def __call__(self, environ: Dict, start_response: Callable):
        setup_testing_defaults(environ)
        path = environ.get('PATH_INFO')
        request = dict()
        # преобразуем данные и наполняем request
        request.update(self.get_request_data(environ))
        logger.info(f'Обработали запрос {request}')
        # from pprint import pprint
        # pprint(request)
        # Проверка вхождения запрошенного пути в список наших роутеров
        if path in self.routes.keys():
            _view = self.routes[path]
        else:
            _view = PageNotFound404()

        for controller in self.controllers:
            controller(request)
        code, body = _view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


"""
{'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br',
 'HTTP_ACCEPT_LANGUAGE': 'ru,en;q=0.9',
 'HTTP_CACHE_CONTROL': 'max-age=0',
 'HTTP_CONNECTION': 'keep-alive',
 'HTTP_HOST': '127.0.0.1:8000',
 'HTTP_SEC_FETCH_DEST': 'document',
 'HTTP_SEC_FETCH_MODE': 'navigate',
 'HTTP_SEC_FETCH_SITE': 'none',
 'HTTP_SEC_FETCH_USER': '?1',
 'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
 'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/88.0.4324.111 '
                    'YaBrowser/21.2.1.94 (beta) Yowser/2.5 Safari/537.36',
 'PATH_INFO': '/',
 'QUERY_STRING': '',
 'RAW_URI': '/',
 'REMOTE_ADDR': '127.0.0.1',
 'REMOTE_PORT': '40384',
 'REQUEST_METHOD': 'GET',
 'SCRIPT_NAME': '',
 'SERVER_NAME': '127.0.0.1',
 'SERVER_PORT': '8000',
 'SERVER_PROTOCOL': 'HTTP/1.1',
 'SERVER_SOFTWARE': 'gunicorn/20.1.0',
 'gunicorn.socket': <socket.socket fd=9, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 40384)>,
 'wsgi.errors': <gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x7f68926e43a0>,
 'wsgi.file_wrapper': <class 'gunicorn.http.wsgi.FileWrapper'>,
 'wsgi.input': <gunicorn.http.body.Body object at 0x7f6892711040>,
 'wsgi.input_terminated': True,
 'wsgi.multiprocess': False,
 'wsgi.multithread': False,
 'wsgi.run_once': False,
 'wsgi.url_scheme': 'http',
 'wsgi.version': (1, 0)}
"""
