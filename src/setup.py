from setuptools import setup, find_packages

setup (
    name='FlightManagementSoftware',
    version='0.1.0',
    packages=find_packages(),
    author='Zion Love',
    install_requires=[
        "tabulate",
        "typing_extensions"
    ],
    entry_points = {
        "console_scripts" : [
            "FlightManagementSoftware = FlightManagementSoftware.clientry:main",
        ]
    },
)