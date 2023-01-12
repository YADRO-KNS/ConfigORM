import setuptools

with open('README.md', "r") as readme:
    long_description = readme.read()


setuptools.setup(
    name="ConfigORM",
    version="1.0.1",
    author="Sergey Parshin",
    author_email="parshinsp@gmail.com",
    description="ORM-like *.ini file and HashiCorp Vault config parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YADRO-KNS/ConfigORM",
    packages=setuptools.find_packages(),
    install_requires=[
        "hvac>=1.0.2"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
