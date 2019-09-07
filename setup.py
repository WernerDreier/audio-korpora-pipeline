#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['SoundFile==0.10.2', 'librosa==0.7.0', 'quantulum3==0.7.2']
setup_requirements = ['pytest-runner']
test_requirements = ['pytest']

setup(
    author="Werner Dreier",
    author_email='***REMOVED***',
    classifiers=[
      'Programming Language :: Python :: 3.7',
    ],
    description="Pipeline for preprocessing audio-corpora for deeplearning such as M-AILABS, Common-Voice and others",
    entry_points={
      'console_scripts': [
        'audio_korpora_pipeline=audio_korpora_pipeline.cli:main',
      ],
    },
    install_requires=requirements,
    license="MIT license': 'License :: OSI Approved :: MIT License",
    long_description="Describe your project here more precisely",
    include_package_data=True,
    name='audio_korpora_pipeline',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='Add your of GIT repo here',
    version='0.1',
)
