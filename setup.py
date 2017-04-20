from distutils.core import setup

setup(
    name='bingraphvis',
    version='0.0.2',
    packages=['bingraphvis', 'bingraphvis.angr', 'bingraphvis.angr.x86', 'bingraphvis.angr.arm'],
    install_requires=[
        'pydot',
        'networkx'
    ],
    description='Visualisation for binary analysis related graphs',
    url='https://github.com/axt/bingraphvis',
)
