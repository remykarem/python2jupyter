import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="p2j",
    version="0.0.2",
    description="Convert Python scripts to Jupyter notebook",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/raibosome/code2notebook",
    author="Raimi bin Karim",
    author_email="raimi.bkarim@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["p2j"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
