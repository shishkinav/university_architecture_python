from jinja2 import Template
from settings import BASE_DIR


def render(template_name, folder='templates', **kwargs):
    """Функция рендеринга шаблонов"""
    file_path = BASE_DIR / folder / template_name
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
