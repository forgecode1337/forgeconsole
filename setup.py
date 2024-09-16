from setuptools import setup, find_packages

setup(
    name='forgeconsole',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'cmd2',
        'colorama',
        'art',
        'pycryptodome',
    ],
    entry_points={
        'console_scripts': [
            'forgeconsole=forgeconsole.cli:main',
        ],
    },
    python_requires='>=3.6',
)
