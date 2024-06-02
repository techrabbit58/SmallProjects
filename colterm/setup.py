from setuptools import setup, find_packages

setup(
    name='colterm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    author='Karl-Dieter Zimmer-Bentin',
    author_email='dzb@pruefbit.de',
    description='Add some convenience to colorama.',
    python_requires='>=3.12',
)
