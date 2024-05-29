""""Setup script for the cinematic_impact_analysis package."""
from setuptools import setup, find_packages


def parse_requirements(filename: str) -> list:
    """
    Parse the requirements file and return a list of requirements.

    :param filename: str: Path to the requirements file
    :return: list: List of requirements
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


setup(
    name='cinematic_impact_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt')
)
