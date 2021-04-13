from jinja2 import Environment, FileSystemLoader
from settings import BASE_DIR


jinja_env = Environment(loader=FileSystemLoader(BASE_DIR / 'templates'))


def render(template_name, **kwargs):
    """Функция рендеринга шаблонов"""
    template = jinja_env.get_template(template_name)
    return template.render(**kwargs)
