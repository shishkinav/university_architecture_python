from frontapp.templates import render
import abc


class BasePage(abc.ABC):
    page_name: str = None

    @abc.abstractmethod
    def __call__(self, request, **kwargs): ...

    def generate_context(self) -> dict:
        return dict(page_name=self.page_name)

class MainPage(BasePage):
    page_name = "Главная"

    def __call__(self, request, **kwargs):
        kwargs['var'] = 'тестик'
        kwargs.update(self.generate_context())
        return '200 OK', render('index.html', **kwargs)


class Contacts(BasePage):
    page_name = "Контакты"

    def __call__(self, request, **kwargs):
        if request.get("method") == 'POST':
            print('Пользователь отправил данные из формы обратной связи:\n '
                  f'{request.get("POST_params")}.\nПозже мы будем здесь вести запись '
                  'в БД этих обращений.')
        kwargs.update(self.generate_context())
        return '200 OK', render('contacts.html', **kwargs)


class AboutPage(BasePage):
    page_name = "О нас"

    def __call__(self, request, **kwargs):
        kwargs.update(self.generate_context())
        return '200 OK', render('about.html', **kwargs)


class PageNotFound404(BasePage):
    page_name = "Страница не найдена"

    def __call__(self, request, **kwargs):
        return '404 WHAT', render('not_found.html', **kwargs)
