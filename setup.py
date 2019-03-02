import subprocess
from setuptools import setup, find_packages
from os.path import dirname, isdir, join

PREFIX = "0.1.%s"

with open(join(dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def get_version():
    path = join(dirname(__file__), ".version")
    if isdir(".git"):
        version = PREFIX % int(subprocess.check_output(["git", "rev-list", "--all", "--count"]))
        with open(path, "w") as f:
            f.write(version)
    else:
        with open(path, "r") as f:
            version = f.read()
    return version


setup(
    name="customidenticon",
    version=get_version(),
    description="Python3 library for generate a variety of identicons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="identicon image avatar profile github custom customidenticon",
    author="LexSerest",
    author_email="lexserest@gmail.com",
    maintainer="LexSerest",
    maintainer_email="lexserest@gmail.com",
    url="https://github.com/lexserest/customidenticon",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pillow",
    ],
)