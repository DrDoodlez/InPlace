from setuptools import setup, find_packages

setup(
    name='InPlcae Management WebApp',
    version='0.2',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests.all_tests",
    install_requires=[
        'flask',
        'Flask-WTF',
        'Flask-SQLAlchemy',
        'alembic',
        'mysql-python',
        'Fabric'
    ]
)
