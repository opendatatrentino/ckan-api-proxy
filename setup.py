import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

version = '0.1-alpha'

install_requires = [
    "flask",
    "flask-restful",
    "ckan-api-client",
]

dependency_links = [
    # "git+https://github.com/rshk/ckan-api-client.git@master#egg=ckan-api-client-0.1-alpha",  # noqa
    "https://github.com/rshk/ckan-api-client/tarball/master#egg=ckan-api-client-0.1-alpha",  # noqa
]

# if sys.version_info < (2, 7):
#     install_requires.append('ordereddict')

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
]

entry_points = {
    'console_scripts': [
        'ckan-api-proxy = ckan_api_proxy.main:main',
    ],
}


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--ignore=build',
            '--verbose',
            # '--cov=ckan_api_client',
            # '--cov-report=term-missing',
            '--pep8',
            'datacat']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='ckan-api-proxy',
    version=version,
    packages=find_packages(),
    url='http://opendatatrentino.github.io/ckan-api-proxy',
    license='BSD License',
    author='Samuele Santi',
    author_email='s.santi@trentorise.eu',
    description='',
    long_description='',
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='ckan_api_proxy.tests',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2.7",
    ],
    package_data={'': ['README.md', 'LICENSE']},
    cmdclass={'test': PyTest},
    entry_points=entry_points,
    dependency_links=dependency_links)
