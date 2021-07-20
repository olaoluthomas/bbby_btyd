# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'pandas==1.2.3', 'numpy==1.20.1', 'Lifetimes==0.11.3', 'dill==0.3.3',
    'flask==2.0.1', 'gunicorn==20.1.0', 'google-cloud-storage==1.40.0',
    'google-cloud-bigquery==2.20.0', 'google-cloud-bigquery-storage==2.6.0'
]

with open("README.md", "r") as fh:
      long_description = fh.read()

setup(name='btyd',
      version='0.1',
      install_requires=REQUIRED_PACKAGES,
      packages=find_packages(),
      include_package_data=True,
      description='Testing custom code for serving BTYD LTV predictions',
      long_description=long_description,
      author='Simeon Thomas',
      licence='MIT',
      zip_safe=False)
