from distutils.core import setup

setup(
    name='bingraphvis',
    version='0.0.1',
    packages=['bingraphvis', 'bingraphvis.angr', 'bingraphvis.angr.x86'],
    install_requires=[
        'pydot',
        'networkx'
    ],
    description='Visualisation for binary analysis related graphs',
    url='https://github.com/axt/bingraphvis',
)
