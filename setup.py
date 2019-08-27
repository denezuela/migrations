from setuptools import setup, find_packages

setup(
    name='test-task',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Test Task',
    author='Denis Zagumennov',
    author_email='zagumionnov.denis@yandex.ru'
)
