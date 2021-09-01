from setuptools import setup, find_packages

setup(
    name="net_test_tools",
    version="0.0.1",
    author="Raiser Ma",
    author_email="mraiser@foxmail.com",
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'udping-master = net_test_tools.scripts.udping_master:udping_master',
        ],
    },
)
