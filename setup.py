from setuptools import setup, find_packages  # type: ignore

with open("README.md") as f:
    long_description = f.read()

setup(
    name="datapatch",
    version="0.2.1",
    author="Friedrich Lindenberg",
    author_email="friedrich@pudo.org",
    url="https://github.com/pudo/datapatch",
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
        "dev": ["pytest", "pytest-cov", "bump2version"],
    },
    entry_points={},
)
