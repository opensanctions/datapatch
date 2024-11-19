from setuptools import setup, find_packages  # type: ignore

with open("README.md") as f:
    long_description = f.read()

setup(
    name="datapatch",
    version="1.2.2",
    author="Friedrich Lindenberg",
    author_email="tech@opensanctions.org",
    url="https://github.com/opensanctions/datapatch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    namespace_packages=[],
    include_package_data=True,
    package_data={},
    zip_safe=False,
    install_requires=[
        "babel >= 2.9.1, < 3.0.0",
        "normality >= 2.1.1, < 3.0.0",
        "pyyaml",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "mypy",
            "types-pyyaml",
            "bump2version",
        ],
    },
    entry_points={},
)
