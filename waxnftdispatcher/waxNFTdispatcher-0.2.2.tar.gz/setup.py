# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waxnftdispatcher']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'pyntelope>=0.7.0,<0.8.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'waxnftdispatcher',
    'version': '0.2.2',
    'description': 'This library will help you to transfer or to mint NFTs on the WAX blockchain',
    'long_description': '# waxNFTdispatcher\n\nThis library will help you to transfer or to mint NFTs on the WAX blockchain. It relies on the library \npyntelope for blockchain interaction and on the library loguru for beautiful logs.\n\n\n## Installation\n```poetry add waxNFTdispatcher```\n\nor\n\n```pip install waxNFTdispatcher```\n\n## Usage\n\n```python\nfrom waxNFTdispatcher import AssetSender\nimport os\n\nprivate_key = os.environ["PRIVATE_KEY"]\ncollection_wallet = "mywallet.wam"\ncollection = "pixeltycoons"\nrecipient = "recipient.wam"\nINPUT = (("rawmaterials", 318738), ("magmaterials", 416529))\n\n# Create object\nassetsender = AssetSender(collection, collection_wallet, private_key)\n\n# Try to find assets in the collection wallet to send them.\n# If not all needed assets were in the collection wallet, the script will mint the rest.\nassetsender.send_or_mint_assets(INPUT, recipient)\n\n# Send assets with given asset ID to the given wallet\nassetsender.send_assets(("1099543811405", "1099543811406"), recipient)\n\n# Mint given number of same assets\nassetsender.mint_assets("rawmaterials", 318738, "recipient.wam", 5)\n```\n\n## Contribution\nContribution is highly welcome. Please send your pull requests or create issues with found bugs and suggestions. \nIn your pull requests please use Black formatting.',
    'author': 'Amparo Dios',
    'author_email': 'amparo.dios@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alparo/waxNFTdispatcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
