"""Backward-compatible setup.py for older pip versions."""

from setuptools import setup, find_packages

setup(
    name="diagramcraft",
    version="0.1.0",
    description="A CLI diagram drawing tool powered by Mermaid.js",
    long_description=open("README_EN.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="DiagramCraft Contributors",
    license="MIT",
    python_requires=">=3.9",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "diagramcraft": ["templates/*.mmd"],
    },
    install_requires=[
        "typer[all]>=0.9.0",
        "rich>=13.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0"],
    },
    entry_points={
        "console_scripts": [
            "diagramcraft=diagramcraft.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ],
    keywords="diagram mermaid flowchart architecture cli visualization",
)
