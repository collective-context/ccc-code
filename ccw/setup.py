from setuptools import setup, find_packages

setup(
    name='ccc-code',
    version='0.2.0',
    description='CCC CODE eases server management based on WordOps',
    author='Collective Context',
    author_email='info@recode.at',
    url='https://github.com/collective-context/ccc-code',
    packages=find_packages(),
    install_requires=[
        'cement==2.10.14',  # Pin exact v2 version for stability
        'colorlog',
    ],
    entry_points={
        'console_scripts': [
            'ccc=ccc.cli.main:main',
            # 'cca=cca.cli.main:main',
            # 'wo=wo.cli.main:main',
            # ccb has its own setup-ccb.py with cement v3
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
