from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "fastapi_pypi_proxy",
    version = "0.0.2",
    description="A pypi proxy using fastapi",
    author="xyzou",
    author_email="zouxinyin1992@163.com",
    url="https://github.com/singingplayer/fastapi-pypi-proxy",
    packages=["fastapi_pypi_proxy"],
    install_requires=required,
)