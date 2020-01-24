import os

from setuptools import find_packages, setup


setup(
    name='my-offers',
    version='0.1.0',
    author='Cian Team',
    author_email='python@cian.ru',
    description='МКС: мои объявления для агента',
    entry_points={
        'console_scripts': [
            'my-offers=my_offers.cli:cli',
        ],
    },
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
