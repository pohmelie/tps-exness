from pathlib import Path

from setuptools import find_packages, setup

PACKAGE_ROOT = Path(__file__).parent
VERSION = PACKAGE_ROOT / "version.txt"


def read_requirements(name: str):
    p = PACKAGE_ROOT.joinpath(name)
    reqs = []
    for line in p.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        req = line
        req = req.split("# ")[0].strip()
        reqs.append(req)
    return reqs


setup(
    name="tps-exness",
    version=VERSION.read_text().strip(),
    packages=find_packages(include=["tps_exness*"]),
    package_data={
        "": ["*.txt", "*.html"],
    },
    python_requires=">= 3.8",
    install_requires=read_requirements("requirements/production.txt"),
    extras_require={
        "dev": read_requirements("requirements/dev.txt"),
    },
)