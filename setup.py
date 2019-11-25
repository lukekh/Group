import setuptools
import groupy

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="groupy",
    version=groupy.__version__,
    author=groupy.__author__,
    author_email="",
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
