import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-dataporten',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A simple Django app to fetch and parse data from Dataporten.',
    long_description=README,
    url='https://github.com/JakobGM/django-dataporten',
    author='Jakob Gerhard Martinussen',
    author_email='jakobgm@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    ],
    install_requires=[
        'django<=2.0',
        'pip-tools',
        'pytest',
        'pytest-django',
        'requests',
        'requests-cache',
        'responses',
        'mypy',
        'mypy_extensions',
        'freezegun',
        'factory_boy',
        'django-allauth'
    ]
)