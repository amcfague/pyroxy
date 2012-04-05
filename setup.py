from setuptools import setup, find_packages

setup(
    name='pyroxy',
    version='0.1',
    description='A proxy for accessing PyPI',
    author='Andrew McFague',
    author_email='amcfague@gmail.com',
    url='https://github.com/amcfague/pyroxy',
    packages=find_packages("src", exclude=['pyroxy.tests', 'pyroxy.tests.*']),
    package_data={'': ['*.tpl']},
    package_dir={'': 'src'},
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=["bottle", "lxml"],
    setup_requires=['nose'],
    tests_require=["coverage", "mock", "webtest"],
)
