"""
Setup configuration for CCC Beta (ccb)
Cement v3 based installation
"""

from setuptools import setup, find_packages

# Read version from ccb/core/version.py
VERSION = '0.1.0'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ccb',
    version=VERSION,
    description='CCC Beta - Experimental tools for CCC CODE development',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='collective-context',
    author_email='info@collective-context.org',
    url='https://github.com/collective-context/ccc-code',
    license='MIT',
    packages=find_packages(exclude=['tests*', 'docs*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ccb = ccb.main:main',
        ],
    },
    install_requires=[
        'cement>=3.0.0,<4.0.0',
        'colorlog',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
)
