import sys
import os
from pathlib import Path
from distutils.core import setup

# scripts should be placed in the scripts dir
scripts = list(Path("scripts").glob("**/*.py"))
[os.system(f"chmod +x {script}") for script in scripts]

setup(
    name="Scritpiboiz from Rob and Jacob",
    version="0.1",
    description="Oh yeah",
    author="Jacob Brady and Rob Harkness",
    packages=["dls"],
    scripts=scripts,
    #package_data={"nmrsa": ["templates/*"]},
)
