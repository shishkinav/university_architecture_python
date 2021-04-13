from frontapp.templates import render


class MainPage:
    def __call__(self, request, **kwargs):
        kwargs['var'] = 'тестик'
        return '200 OK', render('index.html', **kwargs)


class Contacts:
    def __call__(self, request, **kwargs):
        return '200 OK', render('contacts.html', **kwargs)


class PageNotFound404:
    def __call__(self, request, **kwargs):
        return '404 WHAT', render('not_found.html', **kwargs)