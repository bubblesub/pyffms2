from pathlib import Path

from setuptools import find_packages, setup

setup(
    author="spirit",
    author_email="hiddenspirit@gmail.com",
    name="ffms2",
    version="0.4.2",
    description="Bindings for FFmpegSource",
    long_description=(Path(__file__).parent / "README.rst").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/rr-/pyffms2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
    ],
    python_requires=">=3.2",
    packages=find_packages(),
    package_dir={"ffms2": "ffms2"},
    package_data={"ffms2": ["ffms2/*.*"]},
    install_requires=["numpy"],
)
