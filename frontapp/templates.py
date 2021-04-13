from jinja2 import Environment, FileSystemLoader
from settings import BASE_DIR


jinja_env = Environment(loader=FileSystemLoader(BASE_DIR / 'templates'))
jinja_env.globals.update(
    {'static': BASE_DIR / 'static',
     'STATIC_PREFIX': BASE_DIR / 'static'}
)


def render(template_name, **kwargs):
    """Функция рендеринга шаблонов"""
    template = jinja_env.get_template(template_name)
    return template.render(**kwargs)
