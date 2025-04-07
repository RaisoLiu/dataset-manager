from setuptools import setup, find_packages

setup(
    name="dataset-manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "tqdm",
    ],
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for managing and verifying datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dataset-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 