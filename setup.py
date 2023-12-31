import os
from setuptools import setup

# Read the contents of the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Initialize an empty list for the installation requirements
install_requires = []

# Check if a requirements.txt file exists and if so, read its contents
if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as f:
        install_requires = f.read().splitlines()

# Define the package setup configuration
setup(
    name='Easy Lightning',  # Replace with your package name
    packages=['exp_utils', 'data_utils', 'torch_utils'],  # List of all packages included in your project
    description='Easy Lightning: Simplify AI-Deep learning with PyTorch Lightning',  
    long_description=long_description,  # Use the contents of README.md as the long description
    long_description_content_type="text/markdown",
    version='0.0.1',  # Specify the version of your package
    install_requires=install_requires,  # List of required dependencies
    url='https://github.com/fed21',  # Replace with the URL of your GitHub repository
    author='Federico Siciliano, Federico Carmignani',
    author_email='siciliano@diag.uniroma1.it, carmignanifederico@gmail.com',
    keywords=['DeepLearning', 'MachineLearning', 'PyTorch', 'Lightning', 'AI']  # Keywords related to your package
)
