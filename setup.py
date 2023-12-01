# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from shutil import copy2

# load README.md/README.rst file
try:
    if os.path.exists("README.md"):
        with open("README.md", "r") as fp:
            readme = fp.read()
            readme_type = "text/markdown; charset=UTF-8"
    elif os.path.exists("README.rst"):
        with open("README.rst", "r") as fp:
            readme = fp.read()
            readme_type = "text/x-rst; charset=UTF-8"
    else:
        readme = ""
except Exception:
    readme = ""

setup_args = {
    "name": "ndx-pinto-metadata",
    "version": "0.1.2",
    "description": "The NWB extension for storing ViRMEN experimental metadata for the Pinto lab.",
    "long_description": readme,
    "long_description_content_type": readme_type,
    "author": "Szonja Weigl",
    "author_email": "szonja.weigl@catalystneuro.com",
    "url": "",
    "license": "MIT",
    "install_requires": [
        "pynwb>=1.5.0,<3",
        "hdmf>=2.5.6,<4",
    ],
    "packages": find_packages("src/pynwb", exclude=["tests", "tests.*"]),
    "package_dir": {"": "src/pynwb"},
    "package_data": {
        "ndx_pinto_metadata": [
            "spec/ndx-pinto-metadata.namespace.yaml",
            "spec/ndx-pinto-metadata.extensions.yaml",
        ]
    },
    "classifiers": [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
    ],
    "keywords": ["NeurodataWithoutBorders", "NWB", "nwb-extension", "ndx-extension"],
    "zip_safe": False,
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, "spec", "ndx-pinto-metadata.namespace.yaml")
    ext_path = os.path.join(project_dir, "spec", "ndx-pinto-metadata.extensions.yaml")

    dst_dir = os.path.join(project_dir, "src", "pynwb", "ndx_pinto_metadata", "spec")
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == "__main__":
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)
