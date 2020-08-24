import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycscart", # Replace with your own username
    version="0.5.0",
    author="richard_ma",
    author_email="richard.ma.19850509@gmail.com",
    description="package for cs-cart API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richard-ma/pycscart",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.6',
)
