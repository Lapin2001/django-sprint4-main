import sys
from pathlib import Path

from django.test.runner import DiscoverRunner

# Добавляем родительскую директорию в Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


class TestRunner(DiscoverRunner):
    pass
