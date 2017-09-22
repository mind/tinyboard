from setuptools import setup, find_packages

__version__ = '0.1.0'

requires = [
    'numpy>=1.13.1',
    'pillow>=4.2.1',
]

pytorch_requires = ['torch']

setup(
    name='tinyboard',
    version=__version__,
    description='Universal TensorBoard visualization library',
    author='TinyMind',
    author_email='hello@tinymind.ai',
    url='https://github.com/mind/tinyboard',
    packages=find_packages(exclude=('tests', 'tests.*',)),
    install_requires=requires,
    extras_require={
        'pytorch': pytorch_requires,
    },
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
