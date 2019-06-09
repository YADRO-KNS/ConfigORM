import setuptools

with open('README.md', "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="ConfigORM",
    version="0.0.1",
    author="Sergey Parshin",
    author_email="parshinsp@gmail.com",
    description="ORM-like *.ini config parser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YADRO-KNS/ConfigORM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
