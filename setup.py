from setuptools import find_packages, setup

setup(
    name="tfrecord-converter",
    version="0.0.1",
    description="Covert CSV, TSV files to TFRecord and upload to Google Cloud Storage automatically",
    install_requires=[],
    url="https://github.com/harrydrippin/tfrecord-converter.git",
    author="Seunghwan Hong",
    author_email="harrydrippin@gmail.com",
    packages=find_packages(exclude=["tests"]),
)
