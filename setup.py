from setuptools import setup, find_packages

setup(
    name='packages_licences',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click','pandas','bs4','requests','tqdm'
    ],
    entry_points='''
        [console_scripts]
        get_licences=packages_licences.scripts.get_licences:cli
    ''',
)
