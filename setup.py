#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gmail-interactive-client",
    version="1.0.0",
    author="Gmail Client Developer",
    author_email="developer@example.com",
    description="Interactive Gmail client with smart search and date filtering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gmail-interactive-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gmail-client=main:main",
            "gmc=main:main",  # Short alias
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
