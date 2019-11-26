import setuptools
import __init__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="groupy",
    version=__init__.__version__,
    author=__init__.__author__,
    author_email="groupython@gmail.com",
    description="A python package that will allow you to sandbox groups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukekh/groupy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
