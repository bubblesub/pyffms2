import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

install_packages = ["numpy"]
if os.name == "nt" and "[GCC" not in sys.version:
    install_packages.append("pypiwin32")

libs = ["ffms2.dll", "ffms2.lib", "ffmsindex.exe"]
data_libs = []

if set(["bdist_wheel", "--plat-name", "win_amd64"]) <= set(sys.argv) or (
    os.name == "nt" and all([os.path.exists(f) for f in libs])
):
    data_libs = [("Scripts", libs)]

setup(
    author="spirit",
    author_email="hiddenspirit@gmail.com",
    name="ffms2",
    version="0.4.5.4",
    description="Bindings for FFmpegSource",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/bubblesub/pyffms2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    data_files=data_libs,
    python_requires=">=3.7",
    packages=find_packages(),
    package_dir={"ffms2": "ffms2"},
    package_data={"ffms2": ["data/*", "../COPYING", "../COPYING.LESSER"]},
    install_requires=install_packages,
)
