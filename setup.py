#!/usr/bin/env python
"""Setup script for Ethical Hacking AI Agent."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ethical_hacking_ai_agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated security testing tool for static analysis of website source code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ethical_hacking_ai_agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ethical-hacking-agent=src.main:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)