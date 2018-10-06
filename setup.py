from distutils.core import setup

setup(
    name='prometheus_aioredis_metric_extractor',
    packages=['prometheus_aioredis_metric_extractor'],
    version='0.1.0',
    description='',
    author='Belousov Alex',
    author_email='belousov.aka.alfa@gmail.com',
    url='https://github.com/belousovalex/prometheus_aioredis_metric_extractor',
    install_requires=[
        'prometheus_aioredis_client>=0.1.0,<0.2.0',
        'aiohttp>=3.4.4,<4.0.0'
    ],
    license='Apache 2',
)