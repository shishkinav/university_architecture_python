import os
from pathlib import Path


DEBUG = True if int(os.getenv('DEBUG')) else False
BASE_DIR = Path.cwd()