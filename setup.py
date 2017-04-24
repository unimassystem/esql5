from setuptools import setup, find_packages


requires = ['elasticsearch>=5.3.0',
            'Flask>=0.12.0',
            'PyYAML>=3.12',
            'tabulate>=0.7.0',
            'prompt_toolkit>=1.0.14',
            'ply>=3.9',
            'pygments>=2.2.0',
            ] 


setup(
    include_package_data = True,
    name = "esql5",
    version = "0.1",
    packages = find_packages(),
    install_requires = requires,
    author = "qs",
    author_email = "qs@hzhz.co    ",
    description = "Sql on Elasticsearch",
    license = "PSF",
    url = "http://www.hzhz.co",

)
