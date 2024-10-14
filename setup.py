from setuptools import setup, find_packages

setup(
    name='duplicate_finder',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ccdupe=duplicate_finder:main',
        ],
    },
    install_requires=[
        # 필요한 패키지 리스트
    ],
    author='amansman77',
    description='A command-line tool to find and remove duplicate files.',
    url='https://github.com/amansman77/codingtest-duplicate-file-finder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)