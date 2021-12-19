import os

from setuptools import setup, find_packages


def get_version(package_path):
    """Возвращает версию пакета без импорта"""
    _locals = {}
    with open(os.path.join(package_path, '_version.py')) as fp:
        exec(fp.read(), None, _locals)
    return _locals['__version__']


version = get_version('check_list')

setup(
    name='check_list_7495',
    version=version,
    packages=find_packages('.'),
    package_dir={'': '.'},
    python_requires='>=3.7',
    install_requires=[
        'SQLAlchemy~=1.4.18',
        'sqlalchemy-utils~=0.37.8',
        'alembic~=1.5.2',
        'pydantic~=1.7.3',
        'pydantic[dotenv]~=1.7.3',
        'gunicorn~=20.0.4',
        'gevent~=21.1.2',
        'falcon-cors~=1.1.7',
        'passlib~=1.7.4',
        'JSON-log-formatter~=0.3.1',
        'pytz~=2021.3',
        'pandas~=1.1.5',
        'pdfminer.six~=20181108',
        'pdfminer2~=20151206',
        'tabula-py~=2.2.0',
        'chardet~=4.0.0',
        'progressbar~=2.5',
        'xlrd~=1.2.0',
        'openpyxl~=3.0.7',
        'dateparser~=1.0.0',

    ],
    extras_require={
        'dev': [
            'pytest~=6.2.2',
            'pytest-cov~=2.11.1',
            'requests~=2.25.1',
        ]
    }
)
