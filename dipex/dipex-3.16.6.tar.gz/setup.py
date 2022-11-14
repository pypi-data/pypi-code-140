# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['integrations',
 'integrations.SD_Lon.sdlon',
 'integrations.SD_Lon.tests',
 'integrations.aarhus',
 'integrations.aarhus.tests',
 'integrations.ad_integration',
 'integrations.ad_integration.tests',
 'integrations.ad_integration.username_rules',
 'integrations.adtreesync',
 'integrations.adtreesync.tests',
 'integrations.ballerup',
 'integrations.brøndby',
 'integrations.calculate_primary',
 'integrations.calculate_primary.tests',
 'integrations.dar_helper',
 'integrations.egedal',
 'integrations.fkorg_it_systems',
 'integrations.gir.initial_read',
 'integrations.hjørring',
 'integrations.holstebro',
 'integrations.kle',
 'integrations.næstved',
 'integrations.opus',
 'integrations.opus.org_tree_print',
 'integrations.opus.tests',
 'integrations.related_units',
 'integrations.rundb',
 'integrations.rundb.tests',
 'integrations.viborg',
 'sdlon',
 'sql_export',
 'sql_export.tests']

package_data = \
{'': ['*'],
 'integrations': ['SD_Lon/*', 'SD_Lon/init/*', 'requirements/*'],
 'integrations.SD_Lon.tests': ['fixtures/tar_gz1/opt/dipex/os2mo-data-import-and-export/*',
                               'fixtures/tar_gz2/opt/dipex/os2mo-data-import-and-export/*'],
 'integrations.calculate_primary': ['requirements/*']}

modules = \
['priority_by_class']
install_requires = \
['Babel>=2.6.0,<3.0.0',
 'Jinja2>=2.10,<3.0',
 'MarkupSafe>=1.1.0,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'Pygments>=2.3.1,<3.0.0',
 'SQLAlchemy>=1.4.31,<2.0.0',
 'Sphinx>=1.8.4,<2.0.0',
 'Unidecode>=1.3.5,<2.0.0',
 'XlsxWriter>=3.0.2,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'alabaster>=0.7.12,<0.8.0',
 'alchemy-mock>=0.4.3,<0.5.0',
 'alembic>=1.7.5,<2.0.0',
 'anytree>=2.6.0,<3.0.0',
 'asciitree>=0.3.3,<0.4.0',
 'black>=22.3.0,<23.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'chardet>=4.0.0,<5.0.0',
 'click-option-group>=0.5.3,<0.6.0',
 'click>=8.0.3,<9.0.0',
 'deepdiff>=5.7.0,<6.0.0',
 'docutils>=0.14,<0.15',
 'fastapi>=0.75.0,<0.76.0',
 'freezegun>=0.3.11,<0.4.0',
 'fs.smbfs>=1.0.3,<2.0.0',
 'glom>=22.1.0,<23.0.0',
 'google-cloud-storage>=2.1.0,<3.0.0',
 'httpx>=0.22.0,<0.23.0',
 'hypothesis>=6.36.1,<7.0.0',
 'idna>=3.3,<4.0',
 'imagesize>=1.1.0,<2.0.0',
 'isort==5.6.4',
 'jmespath>=0.10.0,<0.11.0',
 'jsonschema>=4.4.0,<5.0.0',
 'ldap3>=2.9.1,<3.0.0',
 'lora-utils>=0.1.0,<0.2.0',
 'lxml>=4.7.1,<5.0.0',
 'mimesis>=5.3.0,<6.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'mysqlclient>=2.1.0,<3.0.0',
 'os2mo-dar-client>=1,<2',
 'os2mo-data-import>=3.4.4,<4.0.0',
 'packaging>=19.0,<20.0',
 'pandas>=1.4.0,<2.0.0',
 'parameterized==0.7.4',
 'pika>=1.2.0,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'pymssql>=2.2.4,<3.0.0',
 'pyodbc>=4.0.32,<5.0.0',
 'pyparsing>=2.3.1,<3.0.0',
 'pytest-aioresponses>=0.2.0,<0.3.0',
 'pytest>=6.2.5,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'pywinrm[kerberos]>=0.4.2,<0.5.0',
 'ra-utils>=1.3.2,<2.0.0',
 'raclients>=1.2.4,<2.0.0',
 'ramodels==5.12.0',
 'recommonmark>=0.7.1,<0.8.0',
 'requests-kerberos>=0.14.0,<0.15.0',
 'requests>=2.21.0,<3.0.0',
 'retrying>=1.3.3,<2.0.0',
 'six>=1.12.0,<2.0.0',
 'snowballstemmer>=1.2.1,<2.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0',
 'sphinxcontrib-websupport>=1.1.0,<2.0.0',
 'spsftp>=0.0.1,<0.0.2',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.62.0,<5.0.0',
 'types-python-dateutil>=2.8.9,<3.0.0',
 'wheel>=0.37.1,<0.38.0',
 'xlrd>=2.0.1,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'dipex',
    'version': '3.16.6',
    'description': 'OS2mo-data-import-and-export',
    'long_description': "#################\nOS2MO Data Import\n#################\n\nMagentas officielle repo til integrationer og eksportfunktioner til OS2MO.\n\nFor spørgsmål til koden eller brug af den, er man velkommen til at kontakte\nMagenta ApS <info@magenta.dk>\n\nUsage\n-----\nStart en OS2mo stak vha. `docker-compose`, se detaljer her:\n* https://os2mo.readthedocs.io/en/1.16.1/dev/environment/docker.html?#docker-compose\n\nDipex' dockerimage kan bygges med `docker-compose build`.\nNår dette er sket, kan DIPEX kommandoer kaldes med fx:\n```\ndocker-compose run --rm dipex python3 metacli.py \n```\nAlternativt kan man starte et udviklingsmiljø med:\n```\ndocker-compose up -d --build\n```\nNår kommandoen er kørt færdig, kan man hoppe ind i containeren med:\n```\ndocker-compose exec dipex /bin/bash\n```\nDette giver en terminal i containeren, hvorfra diverse programmer kan køres.\nEt fælles entrypoint til programmerne findes ved at køre:\n```\npython3 metacli.py\n```\nForbindelsen imod OS2mo, kan testes med programmet: `check_connectivity`:\n```\npython3 metacli.py check_connectivity --mora-base http://mo\n```\n\nDependencies\n------------\nDer bruges poetry til at håndtere pakker. For at sikre at all bruger samme version kan man gøre det gennem docker, fx:\n\n```\ndocker-compose run --rm dipex poetry update\n```\nFor at dette kan virke er filerne pyproject.toml og poetry.lock mountet med skriveadgang i docker-compose.yml.",
    'author': 'Magenta ApS',
    'author_email': 'info@magenta.dk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
