"""
Setup script for Python CLI Framework
Built by Jackson Studio
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python-cli-framework",
    version="1.0.0",
    author="Jackson Studio",
    author_email="[email protected]",
    description="Production-ready Python CLI framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackson-studio/python-cli-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0",
        "packaging>=21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cli-tool=cli.cli:main",
        ],
    },
)
