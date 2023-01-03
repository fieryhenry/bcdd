import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("src/bcdd/files/version.txt", "r", encoding="utf-8") as fh:
    version = fh.read()

setuptools.setup(
    name="bcdd",
    version=version,
    author="fieryhenry",
    description="A tool for decrypting and encrypting battle cats .dat files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fieryhenry/bcdd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "colored",
        "pycryptodomex",
        "requests",
    ],
    include_package_data=True,
    extras_require={
        "testing": [
            "pytest",
            "pytest-cov",
        ],
    },
    package_data={"bcdd": ["py.typed"]},
    flake8={"max-line-length": 160},
)
