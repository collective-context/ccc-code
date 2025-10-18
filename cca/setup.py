
import glob
import os
import sys

from setuptools import find_packages, setup

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG = f.read()

conf = []
templates = []

for name in glob.glob('config/plugins.d/*.conf'):
    conf.insert(1, name)

for name in glob.glob('cca/cli/templates/*.mustache'):
    templates.insert(1, name)

if os.geteuid() == 0:
    if not os.path.exists('/var/log/cca/'):
        os.makedirs('/var/log/cca/')

    if not os.path.exists('/var/lib/cca/tmp/'):
        os.makedirs('/var/lib/cca/tmp/')

setup(name='cccode',
      version='3.22.0',
      description='CCC eases server management and orchestrates AI agents',
      long_description=LONG,
      long_description_content_type='text/markdown',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Natural Language :: German",
          "Topic :: System :: Systems Administration",
      ],
      keywords='server automation CCC ai deployment CLI',
      author='recode@ /YOU ❤️',
      author_email='code@recode.at',
      url='https://github.com/collective-context/ccc-code',
      license='MIT',
      project_urls={
          'Docu/Forum': 'https://ccc.recode.at',
          'Source': 'https://github.com/collective-context/ccc-code',
          'Tracker': 'https://https://github.com/collective-context/ccc-code/issues',
      },
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests',
                                      'templates']),
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      python_requires='>=3.4',
      install_requires=[
          # Required to build documentation
          # "Sphinx >= 1.0",
          # Required to function
          'cement == 2.10.14',
          'pystache',
          'pynginxconfig',
          'PyMySQL >= 1.0.2',
          'psutil',
          'sh',
          'SQLAlchemy == 1.4.54',
          'requests',
          'distro',
          'argcomplete',
          'colorlog',
      ],
      extras_require={  # Optional
          'testing': ['nose', 'coverage'],
      },
      data_files=[('/etc/cca', ['config/cca.conf']),
                  ('/etc/cca/plugins.d', conf),
                  ('/usr/lib/cca/templates', templates),
                  ('/etc/bash_completion.d/',
                   ['config/bash_completion.d/cca_auto.rc']),
                  ('/usr/share/man/man8/', ['docs/cca.8'])],
      setup_requires=[],
      entry_points="""
          [console_scripts]
          cca = cca.cli.main:main
      """,
      namespace_packages=[],
      )
