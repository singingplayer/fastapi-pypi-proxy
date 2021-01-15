from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name = "fastapi_pypi_proxy",
    version = "0.0.2",
    description="A pypi proxy using fastapi",
    long_description=long_description,
    author="xyzou",
    author_email="zouxinyin1992@163.com",
    url="https://github.com/singingplayer/fastapi-pypi-proxy",
    python_requires='>3.6.0',
    packages=["fastapi_pypi_proxy"],
    install_requires=install_requires,
)