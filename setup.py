from distutils.core import setup

setup(
    name='Mirador',
    version='0.1.0',
    author='Nick Jacob - Mirador',
    author_email='nick@mirador.im',
    packages=['mirador', 'mirador.test'],
    scripts=['bin/mirador-client.py'],
    url='http://github.com/mirador-cv/mirador-py',
    license='LICENSE.txt',
    description='client for the Mirador image moderation API. (mirador.im)',
    install_requires=[
        "requests >= 2.3.0"
    ],
)