from setuptools import setup, find_packages

setup(
    name='ttbot',
    version='0.0.2',
    description='Framework to build bots for TikTok',
    url='https://github.com/lukew3/ttbot',
    author='Luke Weiler',
    author_email='lukew25073@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
)
