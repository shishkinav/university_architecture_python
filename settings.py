import os
import logging
from pathlib import Path


DEBUG = True if int(os.getenv('DEBUG')) else False
BASE_DIR = Path.cwd()
STATIC_URL = BASE_DIR / 'static'

if not Path.is_dir(BASE_DIR / 'logs'):
    Path.mkdir(BASE_DIR / 'logs')
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
