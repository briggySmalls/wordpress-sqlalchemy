from setuptools import setup, find_packages

setup(
    name = "wordpress-sqlalchemy",
    version = "0.1",
    url = 'https://github.com/alfredo/wordpress-sqlalchemy',
    license = '',
    description = 'This is a set of SQLAlchemy bindings to the WordPress schema',
    author = 'Dave Benjamin',
    packages = find_packages('.'),
    package_dir = {'': '.'},
    install_requires = ['setuptools', 'sqlalchemy'],
)