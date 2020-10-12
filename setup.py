import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="experiencecloudapis",
    version="1.2.0",
    author="DHL Web Analytics",
    author_email="analytics@dpdhl.com",
    license='MIT',
    description="Adobe Experience Cloud APIs Implementation for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['requests', 'pandas', 'PyJWT', 'cryptography']
)
