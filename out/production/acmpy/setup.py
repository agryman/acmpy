from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='acmpy',
    version='0.0.10',
    author='Arthur Ryman',
    author_email='arthur.ryman@gmail.com',
    description='The Algebraic Collective Model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/agryman/acmpy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10'
)
