import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="groupy",
    version="0.0.3",
    author="lukekh",
    author_email="groupython@gmail.com",
    description="A python package that will allow you to create a sandbox for groups",
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
