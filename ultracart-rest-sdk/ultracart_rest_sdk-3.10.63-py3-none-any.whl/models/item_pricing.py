# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ItemPricing(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'allow_arbitrary_cost': 'bool',
        'arbitrary_cost_velocity_code': 'str',
        'auto_order_cost': 'float',
        'automatic_pricing_tier_name': 'str',
        'automatic_pricing_tier_oid': 'int',
        'cogs': 'float',
        'cost': 'float',
        'currency_code': 'str',
        'manufacturer_suggested_retail_price': 'float',
        'maximum_arbitrary_cost': 'float',
        'minimum_advertised_price': 'float',
        'minimum_arbitrary_cost': 'float',
        'mix_and_match_group': 'str',
        'mix_and_match_group_oid': 'int',
        'sale_cost': 'float',
        'sale_end': 'str',
        'sale_start': 'str',
        'tiers': 'list[ItemPricingTier]'
    }

    attribute_map = {
        'allow_arbitrary_cost': 'allow_arbitrary_cost',
        'arbitrary_cost_velocity_code': 'arbitrary_cost_velocity_code',
        'auto_order_cost': 'auto_order_cost',
        'automatic_pricing_tier_name': 'automatic_pricing_tier_name',
        'automatic_pricing_tier_oid': 'automatic_pricing_tier_oid',
        'cogs': 'cogs',
        'cost': 'cost',
        'currency_code': 'currency_code',
        'manufacturer_suggested_retail_price': 'manufacturer_suggested_retail_price',
        'maximum_arbitrary_cost': 'maximum_arbitrary_cost',
        'minimum_advertised_price': 'minimum_advertised_price',
        'minimum_arbitrary_cost': 'minimum_arbitrary_cost',
        'mix_and_match_group': 'mix_and_match_group',
        'mix_and_match_group_oid': 'mix_and_match_group_oid',
        'sale_cost': 'sale_cost',
        'sale_end': 'sale_end',
        'sale_start': 'sale_start',
        'tiers': 'tiers'
    }

    def __init__(self, allow_arbitrary_cost=None, arbitrary_cost_velocity_code=None, auto_order_cost=None, automatic_pricing_tier_name=None, automatic_pricing_tier_oid=None, cogs=None, cost=None, currency_code=None, manufacturer_suggested_retail_price=None, maximum_arbitrary_cost=None, minimum_advertised_price=None, minimum_arbitrary_cost=None, mix_and_match_group=None, mix_and_match_group_oid=None, sale_cost=None, sale_end=None, sale_start=None, tiers=None):  # noqa: E501
        """ItemPricing - a model defined in Swagger"""  # noqa: E501

        self._allow_arbitrary_cost = None
        self._arbitrary_cost_velocity_code = None
        self._auto_order_cost = None
        self._automatic_pricing_tier_name = None
        self._automatic_pricing_tier_oid = None
        self._cogs = None
        self._cost = None
        self._currency_code = None
        self._manufacturer_suggested_retail_price = None
        self._maximum_arbitrary_cost = None
        self._minimum_advertised_price = None
        self._minimum_arbitrary_cost = None
        self._mix_and_match_group = None
        self._mix_and_match_group_oid = None
        self._sale_cost = None
        self._sale_end = None
        self._sale_start = None
        self._tiers = None
        self.discriminator = None

        if allow_arbitrary_cost is not None:
            self.allow_arbitrary_cost = allow_arbitrary_cost
        if arbitrary_cost_velocity_code is not None:
            self.arbitrary_cost_velocity_code = arbitrary_cost_velocity_code
        if auto_order_cost is not None:
            self.auto_order_cost = auto_order_cost
        if automatic_pricing_tier_name is not None:
            self.automatic_pricing_tier_name = automatic_pricing_tier_name
        if automatic_pricing_tier_oid is not None:
            self.automatic_pricing_tier_oid = automatic_pricing_tier_oid
        if cogs is not None:
            self.cogs = cogs
        if cost is not None:
            self.cost = cost
        if currency_code is not None:
            self.currency_code = currency_code
        if manufacturer_suggested_retail_price is not None:
            self.manufacturer_suggested_retail_price = manufacturer_suggested_retail_price
        if maximum_arbitrary_cost is not None:
            self.maximum_arbitrary_cost = maximum_arbitrary_cost
        if minimum_advertised_price is not None:
            self.minimum_advertised_price = minimum_advertised_price
        if minimum_arbitrary_cost is not None:
            self.minimum_arbitrary_cost = minimum_arbitrary_cost
        if mix_and_match_group is not None:
            self.mix_and_match_group = mix_and_match_group
        if mix_and_match_group_oid is not None:
            self.mix_and_match_group_oid = mix_and_match_group_oid
        if sale_cost is not None:
            self.sale_cost = sale_cost
        if sale_end is not None:
            self.sale_end = sale_end
        if sale_start is not None:
            self.sale_start = sale_start
        if tiers is not None:
            self.tiers = tiers

    @property
    def allow_arbitrary_cost(self):
        """Gets the allow_arbitrary_cost of this ItemPricing.  # noqa: E501

        Allow arbitrary cost  # noqa: E501

        :return: The allow_arbitrary_cost of this ItemPricing.  # noqa: E501
        :rtype: bool
        """
        return self._allow_arbitrary_cost

    @allow_arbitrary_cost.setter
    def allow_arbitrary_cost(self, allow_arbitrary_cost):
        """Sets the allow_arbitrary_cost of this ItemPricing.

        Allow arbitrary cost  # noqa: E501

        :param allow_arbitrary_cost: The allow_arbitrary_cost of this ItemPricing.  # noqa: E501
        :type: bool
        """

        self._allow_arbitrary_cost = allow_arbitrary_cost

    @property
    def arbitrary_cost_velocity_code(self):
        """Gets the arbitrary_cost_velocity_code of this ItemPricing.  # noqa: E501

        Arbitrary cost velocity code  # noqa: E501

        :return: The arbitrary_cost_velocity_code of this ItemPricing.  # noqa: E501
        :rtype: str
        """
        return self._arbitrary_cost_velocity_code

    @arbitrary_cost_velocity_code.setter
    def arbitrary_cost_velocity_code(self, arbitrary_cost_velocity_code):
        """Sets the arbitrary_cost_velocity_code of this ItemPricing.

        Arbitrary cost velocity code  # noqa: E501

        :param arbitrary_cost_velocity_code: The arbitrary_cost_velocity_code of this ItemPricing.  # noqa: E501
        :type: str
        """
        if arbitrary_cost_velocity_code is not None and len(arbitrary_cost_velocity_code) > 10000:
            raise ValueError("Invalid value for `arbitrary_cost_velocity_code`, length must be less than or equal to `10000`")  # noqa: E501

        self._arbitrary_cost_velocity_code = arbitrary_cost_velocity_code

    @property
    def auto_order_cost(self):
        """Gets the auto_order_cost of this ItemPricing.  # noqa: E501

        Cost if customer selects to receive item on auto order.  Set to zero to delete.  # noqa: E501

        :return: The auto_order_cost of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._auto_order_cost

    @auto_order_cost.setter
    def auto_order_cost(self, auto_order_cost):
        """Sets the auto_order_cost of this ItemPricing.

        Cost if customer selects to receive item on auto order.  Set to zero to delete.  # noqa: E501

        :param auto_order_cost: The auto_order_cost of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._auto_order_cost = auto_order_cost

    @property
    def automatic_pricing_tier_name(self):
        """Gets the automatic_pricing_tier_name of this ItemPricing.  # noqa: E501

        Automatic pricing tier name  # noqa: E501

        :return: The automatic_pricing_tier_name of this ItemPricing.  # noqa: E501
        :rtype: str
        """
        return self._automatic_pricing_tier_name

    @automatic_pricing_tier_name.setter
    def automatic_pricing_tier_name(self, automatic_pricing_tier_name):
        """Sets the automatic_pricing_tier_name of this ItemPricing.

        Automatic pricing tier name  # noqa: E501

        :param automatic_pricing_tier_name: The automatic_pricing_tier_name of this ItemPricing.  # noqa: E501
        :type: str
        """

        self._automatic_pricing_tier_name = automatic_pricing_tier_name

    @property
    def automatic_pricing_tier_oid(self):
        """Gets the automatic_pricing_tier_oid of this ItemPricing.  # noqa: E501

        Automatic pricing tier object identifier  # noqa: E501

        :return: The automatic_pricing_tier_oid of this ItemPricing.  # noqa: E501
        :rtype: int
        """
        return self._automatic_pricing_tier_oid

    @automatic_pricing_tier_oid.setter
    def automatic_pricing_tier_oid(self, automatic_pricing_tier_oid):
        """Sets the automatic_pricing_tier_oid of this ItemPricing.

        Automatic pricing tier object identifier  # noqa: E501

        :param automatic_pricing_tier_oid: The automatic_pricing_tier_oid of this ItemPricing.  # noqa: E501
        :type: int
        """

        self._automatic_pricing_tier_oid = automatic_pricing_tier_oid

    @property
    def cogs(self):
        """Gets the cogs of this ItemPricing.  # noqa: E501

        Cost of goods sold  # noqa: E501

        :return: The cogs of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._cogs

    @cogs.setter
    def cogs(self, cogs):
        """Sets the cogs of this ItemPricing.

        Cost of goods sold  # noqa: E501

        :param cogs: The cogs of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._cogs = cogs

    @property
    def cost(self):
        """Gets the cost of this ItemPricing.  # noqa: E501

        Cost  # noqa: E501

        :return: The cost of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this ItemPricing.

        Cost  # noqa: E501

        :param cost: The cost of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def currency_code(self):
        """Gets the currency_code of this ItemPricing.  # noqa: E501

        Currency code  # noqa: E501

        :return: The currency_code of this ItemPricing.  # noqa: E501
        :rtype: str
        """
        return self._currency_code

    @currency_code.setter
    def currency_code(self, currency_code):
        """Sets the currency_code of this ItemPricing.

        Currency code  # noqa: E501

        :param currency_code: The currency_code of this ItemPricing.  # noqa: E501
        :type: str
        """
        if currency_code is not None and len(currency_code) > 3:
            raise ValueError("Invalid value for `currency_code`, length must be less than or equal to `3`")  # noqa: E501

        self._currency_code = currency_code

    @property
    def manufacturer_suggested_retail_price(self):
        """Gets the manufacturer_suggested_retail_price of this ItemPricing.  # noqa: E501

        Manufacturer suggested retail price  # noqa: E501

        :return: The manufacturer_suggested_retail_price of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._manufacturer_suggested_retail_price

    @manufacturer_suggested_retail_price.setter
    def manufacturer_suggested_retail_price(self, manufacturer_suggested_retail_price):
        """Sets the manufacturer_suggested_retail_price of this ItemPricing.

        Manufacturer suggested retail price  # noqa: E501

        :param manufacturer_suggested_retail_price: The manufacturer_suggested_retail_price of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._manufacturer_suggested_retail_price = manufacturer_suggested_retail_price

    @property
    def maximum_arbitrary_cost(self):
        """Gets the maximum_arbitrary_cost of this ItemPricing.  # noqa: E501

        Maximum arbitrary cost  # noqa: E501

        :return: The maximum_arbitrary_cost of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._maximum_arbitrary_cost

    @maximum_arbitrary_cost.setter
    def maximum_arbitrary_cost(self, maximum_arbitrary_cost):
        """Sets the maximum_arbitrary_cost of this ItemPricing.

        Maximum arbitrary cost  # noqa: E501

        :param maximum_arbitrary_cost: The maximum_arbitrary_cost of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._maximum_arbitrary_cost = maximum_arbitrary_cost

    @property
    def minimum_advertised_price(self):
        """Gets the minimum_advertised_price of this ItemPricing.  # noqa: E501

        Minimum advertised price  # noqa: E501

        :return: The minimum_advertised_price of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._minimum_advertised_price

    @minimum_advertised_price.setter
    def minimum_advertised_price(self, minimum_advertised_price):
        """Sets the minimum_advertised_price of this ItemPricing.

        Minimum advertised price  # noqa: E501

        :param minimum_advertised_price: The minimum_advertised_price of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._minimum_advertised_price = minimum_advertised_price

    @property
    def minimum_arbitrary_cost(self):
        """Gets the minimum_arbitrary_cost of this ItemPricing.  # noqa: E501

        Minimum arbitrary cost  # noqa: E501

        :return: The minimum_arbitrary_cost of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._minimum_arbitrary_cost

    @minimum_arbitrary_cost.setter
    def minimum_arbitrary_cost(self, minimum_arbitrary_cost):
        """Sets the minimum_arbitrary_cost of this ItemPricing.

        Minimum arbitrary cost  # noqa: E501

        :param minimum_arbitrary_cost: The minimum_arbitrary_cost of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._minimum_arbitrary_cost = minimum_arbitrary_cost

    @property
    def mix_and_match_group(self):
        """Gets the mix_and_match_group of this ItemPricing.  # noqa: E501

        Mix and match group  # noqa: E501

        :return: The mix_and_match_group of this ItemPricing.  # noqa: E501
        :rtype: str
        """
        return self._mix_and_match_group

    @mix_and_match_group.setter
    def mix_and_match_group(self, mix_and_match_group):
        """Sets the mix_and_match_group of this ItemPricing.

        Mix and match group  # noqa: E501

        :param mix_and_match_group: The mix_and_match_group of this ItemPricing.  # noqa: E501
        :type: str
        """

        self._mix_and_match_group = mix_and_match_group

    @property
    def mix_and_match_group_oid(self):
        """Gets the mix_and_match_group_oid of this ItemPricing.  # noqa: E501

        Mix and match group object identifier  # noqa: E501

        :return: The mix_and_match_group_oid of this ItemPricing.  # noqa: E501
        :rtype: int
        """
        return self._mix_and_match_group_oid

    @mix_and_match_group_oid.setter
    def mix_and_match_group_oid(self, mix_and_match_group_oid):
        """Sets the mix_and_match_group_oid of this ItemPricing.

        Mix and match group object identifier  # noqa: E501

        :param mix_and_match_group_oid: The mix_and_match_group_oid of this ItemPricing.  # noqa: E501
        :type: int
        """

        self._mix_and_match_group_oid = mix_and_match_group_oid

    @property
    def sale_cost(self):
        """Gets the sale_cost of this ItemPricing.  # noqa: E501

        Sale cost  # noqa: E501

        :return: The sale_cost of this ItemPricing.  # noqa: E501
        :rtype: float
        """
        return self._sale_cost

    @sale_cost.setter
    def sale_cost(self, sale_cost):
        """Sets the sale_cost of this ItemPricing.

        Sale cost  # noqa: E501

        :param sale_cost: The sale_cost of this ItemPricing.  # noqa: E501
        :type: float
        """

        self._sale_cost = sale_cost

    @property
    def sale_end(self):
        """Gets the sale_end of this ItemPricing.  # noqa: E501

        Sale end  # noqa: E501

        :return: The sale_end of this ItemPricing.  # noqa: E501
        :rtype: str
        """
        return self._sale_end

    @sale_end.setter
    def sale_end(self, sale_end):
        """Sets the sale_end of this ItemPricing.

        Sale end  # noqa: E501

        :param sale_end: The sale_end of this ItemPricing.  # noqa: E501
        :type: str
        """

        self._sale_end = sale_end

    @property
    def sale_start(self):
        """Gets the sale_start of this ItemPricing.  # noqa: E501

        Sale start  # noqa: E501

        :return: The sale_start of this ItemPricing.  # noqa: E501
        :rtype: str
        """
        return self._sale_start

    @sale_start.setter
    def sale_start(self, sale_start):
        """Sets the sale_start of this ItemPricing.

        Sale start  # noqa: E501

        :param sale_start: The sale_start of this ItemPricing.  # noqa: E501
        :type: str
        """

        self._sale_start = sale_start

    @property
    def tiers(self):
        """Gets the tiers of this ItemPricing.  # noqa: E501

        Tiers  # noqa: E501

        :return: The tiers of this ItemPricing.  # noqa: E501
        :rtype: list[ItemPricingTier]
        """
        return self._tiers

    @tiers.setter
    def tiers(self, tiers):
        """Sets the tiers of this ItemPricing.

        Tiers  # noqa: E501

        :param tiers: The tiers of this ItemPricing.  # noqa: E501
        :type: list[ItemPricingTier]
        """

        self._tiers = tiers

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ItemPricing, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ItemPricing):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
