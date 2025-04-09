from setuptools import setup, find_packages
import os

setup (
    name='FlightManagementSoftware',
    version='0.1.0',
    packages=find_packages(
        where='src'
    ),
    package_dir={ "" : "src"},
    author='Zion Love',
    install_requires=[
        "tabulate",
        "typing_extensions"
    ],
    entry_points = {
        "console_scripts" : [
            "FlightManagementSoftware = FlightManagementSoftware.cli.clientry:main",
        ]
    },
    package_data={
        'FlightManagementSoftware': ['sql/CreateTestData.sql', 'db/database.sqllite3'],
    },
    python_requires=">=3.10"
)