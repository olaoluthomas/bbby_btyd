from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
VERSION = '0.0.1-alpha'

REQUIRED_PACKAGES = [
]

setup(
    name='btyd_demo',
    version=VERSION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olaoluthomas/ltv_btyd_demo",
    project_urls={
        "Bug Tracker": "https://github.com/olaoluthomas/ltv_btyd_demo/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where=("src")),
    package_dir={"": "src"},
    python_requires=">=3.9",
    test_suite="tests"
    install_requires=REQUIRED_PACKAGES,
    zip_safe=True
)
