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


class CartItem(object):
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
        'arbitrary_unit_cost': 'Currency',
        'attributes': 'list[CartItemAttribute]',
        'auto_order_schedule': 'str',
        'default_image_url': 'str',
        'default_thumbnail_url': 'str',
        'description': 'str',
        'discount': 'Currency',
        'extended_description': 'str',
        'item_id': 'str',
        'item_oid': 'int',
        'kit': 'bool',
        'kit_component_options': 'list[CartKitComponentOption]',
        'manufacturer_suggested_retail_price': 'Currency',
        'maximum_quantity': 'float',
        'minimum_quantity': 'float',
        'multimedia': 'list[CartItemMultimedia]',
        'options': 'list[CartItemOption]',
        'phsyical': 'CartItemPhysical',
        'position': 'int',
        'preorder': 'bool',
        'quantity': 'float',
        'schedules': 'list[str]',
        'total_cost': 'Currency',
        'total_cost_with_discount': 'Currency',
        'unit_cost': 'Currency',
        'unit_cost_with_discount': 'Currency',
        'upsell': 'bool',
        'variations': 'list[CartItemVariationSelection]',
        'view_url': 'str'
    }

    attribute_map = {
        'arbitrary_unit_cost': 'arbitrary_unit_cost',
        'attributes': 'attributes',
        'auto_order_schedule': 'auto_order_schedule',
        'default_image_url': 'default_image_url',
        'default_thumbnail_url': 'default_thumbnail_url',
        'description': 'description',
        'discount': 'discount',
        'extended_description': 'extended_description',
        'item_id': 'item_id',
        'item_oid': 'item_oid',
        'kit': 'kit',
        'kit_component_options': 'kit_component_options',
        'manufacturer_suggested_retail_price': 'manufacturer_suggested_retail_price',
        'maximum_quantity': 'maximum_quantity',
        'minimum_quantity': 'minimum_quantity',
        'multimedia': 'multimedia',
        'options': 'options',
        'phsyical': 'phsyical',
        'position': 'position',
        'preorder': 'preorder',
        'quantity': 'quantity',
        'schedules': 'schedules',
        'total_cost': 'total_cost',
        'total_cost_with_discount': 'total_cost_with_discount',
        'unit_cost': 'unit_cost',
        'unit_cost_with_discount': 'unit_cost_with_discount',
        'upsell': 'upsell',
        'variations': 'variations',
        'view_url': 'view_url'
    }

    def __init__(self, arbitrary_unit_cost=None, attributes=None, auto_order_schedule=None, default_image_url=None, default_thumbnail_url=None, description=None, discount=None, extended_description=None, item_id=None, item_oid=None, kit=None, kit_component_options=None, manufacturer_suggested_retail_price=None, maximum_quantity=None, minimum_quantity=None, multimedia=None, options=None, phsyical=None, position=None, preorder=None, quantity=None, schedules=None, total_cost=None, total_cost_with_discount=None, unit_cost=None, unit_cost_with_discount=None, upsell=None, variations=None, view_url=None):  # noqa: E501
        """CartItem - a model defined in Swagger"""  # noqa: E501

        self._arbitrary_unit_cost = None
        self._attributes = None
        self._auto_order_schedule = None
        self._default_image_url = None
        self._default_thumbnail_url = None
        self._description = None
        self._discount = None
        self._extended_description = None
        self._item_id = None
        self._item_oid = None
        self._kit = None
        self._kit_component_options = None
        self._manufacturer_suggested_retail_price = None
        self._maximum_quantity = None
        self._minimum_quantity = None
        self._multimedia = None
        self._options = None
        self._phsyical = None
        self._position = None
        self._preorder = None
        self._quantity = None
        self._schedules = None
        self._total_cost = None
        self._total_cost_with_discount = None
        self._unit_cost = None
        self._unit_cost_with_discount = None
        self._upsell = None
        self._variations = None
        self._view_url = None
        self.discriminator = None

        if arbitrary_unit_cost is not None:
            self.arbitrary_unit_cost = arbitrary_unit_cost
        if attributes is not None:
            self.attributes = attributes
        if auto_order_schedule is not None:
            self.auto_order_schedule = auto_order_schedule
        if default_image_url is not None:
            self.default_image_url = default_image_url
        if default_thumbnail_url is not None:
            self.default_thumbnail_url = default_thumbnail_url
        if description is not None:
            self.description = description
        if discount is not None:
            self.discount = discount
        if extended_description is not None:
            self.extended_description = extended_description
        if item_id is not None:
            self.item_id = item_id
        if item_oid is not None:
            self.item_oid = item_oid
        if kit is not None:
            self.kit = kit
        if kit_component_options is not None:
            self.kit_component_options = kit_component_options
        if manufacturer_suggested_retail_price is not None:
            self.manufacturer_suggested_retail_price = manufacturer_suggested_retail_price
        if maximum_quantity is not None:
            self.maximum_quantity = maximum_quantity
        if minimum_quantity is not None:
            self.minimum_quantity = minimum_quantity
        if multimedia is not None:
            self.multimedia = multimedia
        if options is not None:
            self.options = options
        if phsyical is not None:
            self.phsyical = phsyical
        if position is not None:
            self.position = position
        if preorder is not None:
            self.preorder = preorder
        if quantity is not None:
            self.quantity = quantity
        if schedules is not None:
            self.schedules = schedules
        if total_cost is not None:
            self.total_cost = total_cost
        if total_cost_with_discount is not None:
            self.total_cost_with_discount = total_cost_with_discount
        if unit_cost is not None:
            self.unit_cost = unit_cost
        if unit_cost_with_discount is not None:
            self.unit_cost_with_discount = unit_cost_with_discount
        if upsell is not None:
            self.upsell = upsell
        if variations is not None:
            self.variations = variations
        if view_url is not None:
            self.view_url = view_url

    @property
    def arbitrary_unit_cost(self):
        """Gets the arbitrary_unit_cost of this CartItem.  # noqa: E501


        :return: The arbitrary_unit_cost of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._arbitrary_unit_cost

    @arbitrary_unit_cost.setter
    def arbitrary_unit_cost(self, arbitrary_unit_cost):
        """Sets the arbitrary_unit_cost of this CartItem.


        :param arbitrary_unit_cost: The arbitrary_unit_cost of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._arbitrary_unit_cost = arbitrary_unit_cost

    @property
    def attributes(self):
        """Gets the attributes of this CartItem.  # noqa: E501

        Attributes  # noqa: E501

        :return: The attributes of this CartItem.  # noqa: E501
        :rtype: list[CartItemAttribute]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this CartItem.

        Attributes  # noqa: E501

        :param attributes: The attributes of this CartItem.  # noqa: E501
        :type: list[CartItemAttribute]
        """

        self._attributes = attributes

    @property
    def auto_order_schedule(self):
        """Gets the auto_order_schedule of this CartItem.  # noqa: E501

        Auto order schedule the customer selected  # noqa: E501

        :return: The auto_order_schedule of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._auto_order_schedule

    @auto_order_schedule.setter
    def auto_order_schedule(self, auto_order_schedule):
        """Sets the auto_order_schedule of this CartItem.

        Auto order schedule the customer selected  # noqa: E501

        :param auto_order_schedule: The auto_order_schedule of this CartItem.  # noqa: E501
        :type: str
        """

        self._auto_order_schedule = auto_order_schedule

    @property
    def default_image_url(self):
        """Gets the default_image_url of this CartItem.  # noqa: E501

        URL to the default multimedia image  # noqa: E501

        :return: The default_image_url of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._default_image_url

    @default_image_url.setter
    def default_image_url(self, default_image_url):
        """Sets the default_image_url of this CartItem.

        URL to the default multimedia image  # noqa: E501

        :param default_image_url: The default_image_url of this CartItem.  # noqa: E501
        :type: str
        """

        self._default_image_url = default_image_url

    @property
    def default_thumbnail_url(self):
        """Gets the default_thumbnail_url of this CartItem.  # noqa: E501

        URL to the default multimedia thumbnail  # noqa: E501

        :return: The default_thumbnail_url of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._default_thumbnail_url

    @default_thumbnail_url.setter
    def default_thumbnail_url(self, default_thumbnail_url):
        """Sets the default_thumbnail_url of this CartItem.

        URL to the default multimedia thumbnail  # noqa: E501

        :param default_thumbnail_url: The default_thumbnail_url of this CartItem.  # noqa: E501
        :type: str
        """

        self._default_thumbnail_url = default_thumbnail_url

    @property
    def description(self):
        """Gets the description of this CartItem.  # noqa: E501

        Description of the item  # noqa: E501

        :return: The description of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CartItem.

        Description of the item  # noqa: E501

        :param description: The description of this CartItem.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def discount(self):
        """Gets the discount of this CartItem.  # noqa: E501


        :return: The discount of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._discount

    @discount.setter
    def discount(self, discount):
        """Sets the discount of this CartItem.


        :param discount: The discount of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._discount = discount

    @property
    def extended_description(self):
        """Gets the extended_description of this CartItem.  # noqa: E501

        Extended description of the item  # noqa: E501

        :return: The extended_description of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._extended_description

    @extended_description.setter
    def extended_description(self, extended_description):
        """Sets the extended_description of this CartItem.

        Extended description of the item  # noqa: E501

        :param extended_description: The extended_description of this CartItem.  # noqa: E501
        :type: str
        """

        self._extended_description = extended_description

    @property
    def item_id(self):
        """Gets the item_id of this CartItem.  # noqa: E501

        Item ID  # noqa: E501

        :return: The item_id of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        """Sets the item_id of this CartItem.

        Item ID  # noqa: E501

        :param item_id: The item_id of this CartItem.  # noqa: E501
        :type: str
        """

        self._item_id = item_id

    @property
    def item_oid(self):
        """Gets the item_oid of this CartItem.  # noqa: E501

        Item object identifier  # noqa: E501

        :return: The item_oid of this CartItem.  # noqa: E501
        :rtype: int
        """
        return self._item_oid

    @item_oid.setter
    def item_oid(self, item_oid):
        """Sets the item_oid of this CartItem.

        Item object identifier  # noqa: E501

        :param item_oid: The item_oid of this CartItem.  # noqa: E501
        :type: int
        """

        self._item_oid = item_oid

    @property
    def kit(self):
        """Gets the kit of this CartItem.  # noqa: E501

        True if this item is a kit  # noqa: E501

        :return: The kit of this CartItem.  # noqa: E501
        :rtype: bool
        """
        return self._kit

    @kit.setter
    def kit(self, kit):
        """Sets the kit of this CartItem.

        True if this item is a kit  # noqa: E501

        :param kit: The kit of this CartItem.  # noqa: E501
        :type: bool
        """

        self._kit = kit

    @property
    def kit_component_options(self):
        """Gets the kit_component_options of this CartItem.  # noqa: E501

        Options associated with the kit components  # noqa: E501

        :return: The kit_component_options of this CartItem.  # noqa: E501
        :rtype: list[CartKitComponentOption]
        """
        return self._kit_component_options

    @kit_component_options.setter
    def kit_component_options(self, kit_component_options):
        """Sets the kit_component_options of this CartItem.

        Options associated with the kit components  # noqa: E501

        :param kit_component_options: The kit_component_options of this CartItem.  # noqa: E501
        :type: list[CartKitComponentOption]
        """

        self._kit_component_options = kit_component_options

    @property
    def manufacturer_suggested_retail_price(self):
        """Gets the manufacturer_suggested_retail_price of this CartItem.  # noqa: E501


        :return: The manufacturer_suggested_retail_price of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._manufacturer_suggested_retail_price

    @manufacturer_suggested_retail_price.setter
    def manufacturer_suggested_retail_price(self, manufacturer_suggested_retail_price):
        """Sets the manufacturer_suggested_retail_price of this CartItem.


        :param manufacturer_suggested_retail_price: The manufacturer_suggested_retail_price of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._manufacturer_suggested_retail_price = manufacturer_suggested_retail_price

    @property
    def maximum_quantity(self):
        """Gets the maximum_quantity of this CartItem.  # noqa: E501

        Maximum quantity the customer can purchase  # noqa: E501

        :return: The maximum_quantity of this CartItem.  # noqa: E501
        :rtype: float
        """
        return self._maximum_quantity

    @maximum_quantity.setter
    def maximum_quantity(self, maximum_quantity):
        """Sets the maximum_quantity of this CartItem.

        Maximum quantity the customer can purchase  # noqa: E501

        :param maximum_quantity: The maximum_quantity of this CartItem.  # noqa: E501
        :type: float
        """

        self._maximum_quantity = maximum_quantity

    @property
    def minimum_quantity(self):
        """Gets the minimum_quantity of this CartItem.  # noqa: E501

        Minimum quantity the customer can purchase  # noqa: E501

        :return: The minimum_quantity of this CartItem.  # noqa: E501
        :rtype: float
        """
        return self._minimum_quantity

    @minimum_quantity.setter
    def minimum_quantity(self, minimum_quantity):
        """Sets the minimum_quantity of this CartItem.

        Minimum quantity the customer can purchase  # noqa: E501

        :param minimum_quantity: The minimum_quantity of this CartItem.  # noqa: E501
        :type: float
        """

        self._minimum_quantity = minimum_quantity

    @property
    def multimedia(self):
        """Gets the multimedia of this CartItem.  # noqa: E501

        Multimedia  # noqa: E501

        :return: The multimedia of this CartItem.  # noqa: E501
        :rtype: list[CartItemMultimedia]
        """
        return self._multimedia

    @multimedia.setter
    def multimedia(self, multimedia):
        """Sets the multimedia of this CartItem.

        Multimedia  # noqa: E501

        :param multimedia: The multimedia of this CartItem.  # noqa: E501
        :type: list[CartItemMultimedia]
        """

        self._multimedia = multimedia

    @property
    def options(self):
        """Gets the options of this CartItem.  # noqa: E501

        Options  # noqa: E501

        :return: The options of this CartItem.  # noqa: E501
        :rtype: list[CartItemOption]
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this CartItem.

        Options  # noqa: E501

        :param options: The options of this CartItem.  # noqa: E501
        :type: list[CartItemOption]
        """

        self._options = options

    @property
    def phsyical(self):
        """Gets the phsyical of this CartItem.  # noqa: E501


        :return: The phsyical of this CartItem.  # noqa: E501
        :rtype: CartItemPhysical
        """
        return self._phsyical

    @phsyical.setter
    def phsyical(self, phsyical):
        """Sets the phsyical of this CartItem.


        :param phsyical: The phsyical of this CartItem.  # noqa: E501
        :type: CartItemPhysical
        """

        self._phsyical = phsyical

    @property
    def position(self):
        """Gets the position of this CartItem.  # noqa: E501

        Position of the item in the cart  # noqa: E501

        :return: The position of this CartItem.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this CartItem.

        Position of the item in the cart  # noqa: E501

        :param position: The position of this CartItem.  # noqa: E501
        :type: int
        """

        self._position = position

    @property
    def preorder(self):
        """Gets the preorder of this CartItem.  # noqa: E501

        True if this item is on pre-order  # noqa: E501

        :return: The preorder of this CartItem.  # noqa: E501
        :rtype: bool
        """
        return self._preorder

    @preorder.setter
    def preorder(self, preorder):
        """Sets the preorder of this CartItem.

        True if this item is on pre-order  # noqa: E501

        :param preorder: The preorder of this CartItem.  # noqa: E501
        :type: bool
        """

        self._preorder = preorder

    @property
    def quantity(self):
        """Gets the quantity of this CartItem.  # noqa: E501

        quantity  # noqa: E501

        :return: The quantity of this CartItem.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this CartItem.

        quantity  # noqa: E501

        :param quantity: The quantity of this CartItem.  # noqa: E501
        :type: float
        """

        self._quantity = quantity

    @property
    def schedules(self):
        """Gets the schedules of this CartItem.  # noqa: E501

        Customer selectable auto order schedules  # noqa: E501

        :return: The schedules of this CartItem.  # noqa: E501
        :rtype: list[str]
        """
        return self._schedules

    @schedules.setter
    def schedules(self, schedules):
        """Sets the schedules of this CartItem.

        Customer selectable auto order schedules  # noqa: E501

        :param schedules: The schedules of this CartItem.  # noqa: E501
        :type: list[str]
        """

        self._schedules = schedules

    @property
    def total_cost(self):
        """Gets the total_cost of this CartItem.  # noqa: E501


        :return: The total_cost of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._total_cost

    @total_cost.setter
    def total_cost(self, total_cost):
        """Sets the total_cost of this CartItem.


        :param total_cost: The total_cost of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._total_cost = total_cost

    @property
    def total_cost_with_discount(self):
        """Gets the total_cost_with_discount of this CartItem.  # noqa: E501


        :return: The total_cost_with_discount of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._total_cost_with_discount

    @total_cost_with_discount.setter
    def total_cost_with_discount(self, total_cost_with_discount):
        """Sets the total_cost_with_discount of this CartItem.


        :param total_cost_with_discount: The total_cost_with_discount of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._total_cost_with_discount = total_cost_with_discount

    @property
    def unit_cost(self):
        """Gets the unit_cost of this CartItem.  # noqa: E501


        :return: The unit_cost of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._unit_cost

    @unit_cost.setter
    def unit_cost(self, unit_cost):
        """Sets the unit_cost of this CartItem.


        :param unit_cost: The unit_cost of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._unit_cost = unit_cost

    @property
    def unit_cost_with_discount(self):
        """Gets the unit_cost_with_discount of this CartItem.  # noqa: E501


        :return: The unit_cost_with_discount of this CartItem.  # noqa: E501
        :rtype: Currency
        """
        return self._unit_cost_with_discount

    @unit_cost_with_discount.setter
    def unit_cost_with_discount(self, unit_cost_with_discount):
        """Sets the unit_cost_with_discount of this CartItem.


        :param unit_cost_with_discount: The unit_cost_with_discount of this CartItem.  # noqa: E501
        :type: Currency
        """

        self._unit_cost_with_discount = unit_cost_with_discount

    @property
    def upsell(self):
        """Gets the upsell of this CartItem.  # noqa: E501

        True if this item was added to the cart as part of an upsell  # noqa: E501

        :return: The upsell of this CartItem.  # noqa: E501
        :rtype: bool
        """
        return self._upsell

    @upsell.setter
    def upsell(self, upsell):
        """Sets the upsell of this CartItem.

        True if this item was added to the cart as part of an upsell  # noqa: E501

        :param upsell: The upsell of this CartItem.  # noqa: E501
        :type: bool
        """

        self._upsell = upsell

    @property
    def variations(self):
        """Gets the variations of this CartItem.  # noqa: E501

        Variations  # noqa: E501

        :return: The variations of this CartItem.  # noqa: E501
        :rtype: list[CartItemVariationSelection]
        """
        return self._variations

    @variations.setter
    def variations(self, variations):
        """Sets the variations of this CartItem.

        Variations  # noqa: E501

        :param variations: The variations of this CartItem.  # noqa: E501
        :type: list[CartItemVariationSelection]
        """

        self._variations = variations

    @property
    def view_url(self):
        """Gets the view_url of this CartItem.  # noqa: E501

        URL to view the product on the site  # noqa: E501

        :return: The view_url of this CartItem.  # noqa: E501
        :rtype: str
        """
        return self._view_url

    @view_url.setter
    def view_url(self, view_url):
        """Sets the view_url of this CartItem.

        URL to view the product on the site  # noqa: E501

        :param view_url: The view_url of this CartItem.  # noqa: E501
        :type: str
        """

        self._view_url = view_url

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
        if issubclass(CartItem, dict):
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
        if not isinstance(other, CartItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
