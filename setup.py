from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()


setup(
    name='cinematic_impact_analysis',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt')
)
