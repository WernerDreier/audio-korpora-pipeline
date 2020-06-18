#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['SoundFile==0.10.2', 'librosa==0.7.0', 'quantulum3==0.7.2', 'pandas==0.25.1',
                'ffmpeg-python==0.2.0', 'webrtcvad==2.0.10']
setup_requirements = ['pytest-runner']
test_requirements = ['pytest']

setup(
    author="Werner Dreier",
    author_email='code@wernerdreier.ch',
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
    python_requires='>=3.7.3',
    license="MIT license': 'License :: OSI Approved :: MIT License",
    long_description="Pipeline for preprocessing audio-corpora for deeplearning such as M-AILABS, Common-Voice and others",
    include_package_data=True,
    name='audio_korpora_pipeline',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/WernerDreier/audio-korpora-pipeline.git',
    version='swisstext-SNAPSHOT',
)
