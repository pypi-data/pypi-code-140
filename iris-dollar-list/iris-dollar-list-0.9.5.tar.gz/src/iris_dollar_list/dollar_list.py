# Module that covers the DollarList classes
# DollarListReader and DollarListWriter
# DollarItem is a class that is used by the DollarList classes
# to store the data in a list of objects
#

from dataclasses import dataclass
from enum import Enum
import struct
from typing import Any,List
import decimal

class Dollartype(Enum):
    ITEM_UNDEF = -1
    ITEM_PLACEHOLDER = 0
    ITEM_ASCII = 1
    ITEM_UNICODE = 2
    ITEM_POSINT = 4
    ITEM_NEGINT = 5
    ITEM_POSNUM = 6
    ITEM_NEGNUM = 7
    ITEM_DOUBLE = 8
    ITEM_COMPACT_DOUBLE = 9

@dataclass
class DollarItem:
    """
    A class that represents a dollar item
    """
    # type of the item
    dollar_type: Dollartype = Dollartype.ITEM_UNDEF
    # value of the item
    value: Any = None
    # raw data of the item
    raw_value: bytes = b''
    # raw data of the item + meta data
    buffer: bytes = b''
    # offset of the item in the list buffer
    offset: int = 0
    # length of the item in defined in the meta data
    meta_value_length: int = 0
    # length of the meta data
    meta_offset: int = 0


# create DollarList exceptions
class DollarListException(Exception):
    """
    Base class for DollarList exceptions
    """

class DollarListReader:

    def __init__(self, buffer:bytes):
        self.items = []
        self.buffer = buffer
        self.offset = 0
        self.next_offset = 0
        self.read_buffer()

    def read_buffer(self):
        """
        read the buffer and return a list of DollarItems
        """
        while self.next_offset < len(self.buffer):
            item = self.get_next_item()
            self.items.append(item)

    def get_item_length(self,offset):
        meta_offset = 0
        # if first byte is 0, then length is next 2 bytes
        if self.buffer[offset] == 0:
            length = self.buffer[offset + 1] | (self.buffer[offset + 2] << 8)
            meta_offset = 4
            # if the length is still 0, then the length is the next 4 bytes
            if length == 0:
                length = (
                        self.buffer[offset+3]
                        | (self.buffer[offset + 4] << 8)
                        | (self.buffer[offset + 5] << 16)
                        | (self.buffer[offset + 6] << 24)
                )
                meta_offset = 8
        else:
            length = self.buffer[offset]
            meta_offset = 2
        if length > len(self.buffer) or length <= 0:
            raise ValueError("Invalid length")
        return length, meta_offset

    def get_item_type(self,offset,meta_offset=None):
        if meta_offset is None:
            meta_offset = self.get_item_length(offset)[1]
        typ = self.buffer[offset+meta_offset-1]
            # if result is not between 0 and 9, then raise an exception
        if typ < 0 or typ > 9:
            raise ValueError("Invalid type")
        return typ

    def get_item_raw_value(self,offset,meta_offset=None,length=None):
        result = None
        if meta_offset is None or length is None:
            length, meta_offset = self.get_item_length(offset)
        if meta_offset == 2:
            result = self.buffer[offset+meta_offset:offset+length]
        elif meta_offset > 2:
            result = self.buffer[offset+meta_offset:offset+length+meta_offset-1]
        return result

    def get_item_buffer(self,offset,meta_offset=None,length=None):
        result = None
        if meta_offset is None or length is None:
            length, meta_offset = self.get_item_length(offset)
        if meta_offset == 2:
            result = self.buffer[offset:offset+length]
        elif meta_offset > 2:
            result = self.buffer[offset:offset+length+meta_offset-1]
        return result

    def get_item_value(self,offset,meta_offset=None,length=None,typ=None,raw_value=None):
        val = None
        if meta_offset is None or length is None:
            length, meta_offset = self.get_item_length(offset)
        if typ is None:
            typ = self.get_item_type(
                    offset=offset,
                    meta_offset=meta_offset
                )
        if raw_value is None:
            raw_value = self.get_item_raw_value(offset,meta_offset,length)
        if typ == Dollartype.ITEM_ASCII.value:
            val = self.get_ascii(raw_value)
        elif typ == Dollartype.ITEM_UNICODE.value:
            val = raw_value.decode('utf-16')
        elif typ == Dollartype.ITEM_POSINT.value:
            val = self.get_posint(raw_value)
        elif typ == Dollartype.ITEM_NEGINT.value:
            val = self.get_negint(raw_value)
        elif typ == Dollartype.ITEM_POSNUM.value:
            val = self.get_posnum(raw_value)
        elif typ == Dollartype.ITEM_NEGNUM.value:
            val = self.get_negnum(raw_value)
        elif typ == Dollartype.ITEM_DOUBLE.value:
            val = struct.unpack('<d',raw_value)[0]
        elif typ == Dollartype.ITEM_COMPACT_DOUBLE.value:
            val = struct.unpack('<f',raw_value)[0]
        else:
            val = None
        return val

    def get_ascii(self,raw_value):
        """
        Decode the value as ascii.
        If decoding fails, consider the value as a sub-list.
        If decoding the sub-list fails, consider the value as a binary.
        """
        if raw_value == b'':
            return None
        try:
            return DollarList.from_bytes(raw_value)
        except ValueError:
            try:
                return raw_value.decode('ascii')
            except UnicodeDecodeError:
                return raw_value

    def get_posint(self,raw_value):
        return int.from_bytes(raw_value, "little")

    def get_negint(self,raw_value):
        return int.from_bytes(raw_value, "little",signed=True)

    def get_posnum(self,raw_value):
        num = self.get_posint(raw_value[1:])
        scale = raw_value[0]
        if scale > 127:
            scale -= 256
        decstr = str(num) + "E" + str(scale)
        dec = decimal.Decimal(decstr)
        return float(dec)

    def get_negnum(self,raw_value):
        num = self.get_negint(raw_value[1:])
        scale = raw_value[0]
        if scale > 127:
            scale -= 256
        decstr = str(num) + "E" + str(scale)
        dec = decimal.Decimal(decstr)
        return float(dec)

    def get_item(self,offset) -> DollarItem:
        item = DollarItem()
        item.offset = offset
        item.meta_value_length,item.meta_offset = self.get_item_length(offset)
        item.dollar_type = self.get_item_type(
            offset=offset,
            meta_offset=item.meta_offset,
        )
        item.raw_value = self.get_item_raw_value(offset,item.meta_offset,item.meta_value_length)
        item.buffer = self.get_item_buffer(offset,item.meta_offset,item.meta_value_length)
        item.value = self.get_item_value(offset,item.meta_offset,item.meta_value_length)
        # if value is a list change the typ to ITEM_PLACEHOLDER
        if isinstance(item.value,DollarList):
            item.dollar_type = 0
        return item

    def get_next_item(self) -> DollarItem:
        item = self.get_item(self.next_offset)
        self.next_offset = self.get_next_offset(self.next_offset)
        return item

    def get_next_offset(self,offset,meta_offset=None,length=None):
        response = None
        if meta_offset is None or length is None:
            length, meta_offset = self.get_item_length(offset)
        if meta_offset == 2:
            response = offset + length
        elif meta_offset > 2:
            response = offset + length + meta_offset - 1
        return response

class DollarListWriter:
    """
    Convert a DollarList to it's byte form
    """
    def __init__(self):
        self.dollar_list = []
        self.buffer = b''
        self.offset = 0

    def create_dollar_item(self,item):
        """
        Create a DollarItem from a python object
        Based on the item type convert it
        """
        rsp = None
        if isinstance(item,DollarItem):
            rsp = item
        elif isinstance(item,DollarList):
            rsp = DollarItem(value=item,dollar_type=0,raw_value=item.to_bytes()
            ,buffer=self.get_meta_value_length(item.to_bytes())+
                Dollartype.ITEM_ASCII.value.to_bytes(1, "little")+
                item.to_bytes())
        elif isinstance(item,str) or item is None:
            rsp = self.create_from_string(item)
        elif isinstance(item,int):
            rsp = self.create_from_int(item)
        elif isinstance(item,float):
            rsp = self.create_from_float(item)
        elif isinstance(item,bytes):
            raise DollarListException("Bytes are not supported")
        else:
            raise DollarListException("Invalid item type")
        return rsp

    def create_from_string(self,item):
        """
        Create a DollarItem from a string
        """
        response = DollarItem()
        if item == '' or item is None:
            response = self.create_null_item()
        else:
            try:
                response = self.create_from_ascii(item,'ascii')
            except UnicodeEncodeError:
                try:
                    response = self.create_from_ascii(item,'latin-1')
                except UnicodeEncodeError:
                    response = self.create_from_ascii(item,'utf-16')
        return response

    def create_null_item(self):
        """
        Create a DollarItem with a null value
        """
        raw_value = b''
        item_value = None
        lenght = b'\x02'
        buffer = lenght + Dollartype.ITEM_ASCII.value.to_bytes(1, "little") + raw_value
        return DollarItem(
            value=item_value,
            raw_value=raw_value,
            buffer=buffer,
            dollar_type=Dollartype.ITEM_ASCII.value,
        )

    def create_from_ascii(self,item,locale):
        """
        Create a DollarItem from a string
        """
        raw_value = item.encode(locale)
        item_value = item
        lenght = self.get_meta_value_length(raw_value)
        if locale != 'utf-16':
            typ = Dollartype.ITEM_ASCII.value
        else:
            typ = Dollartype.ITEM_UNICODE.value
        buffer = lenght + typ.to_bytes(1, "little") + raw_value
        return DollarItem(
            value=item_value,
            raw_value=raw_value,
            buffer=buffer,
            dollar_type=typ,
        )

    def create_from_int(self,item):
        """
        Create a DollarItem from an integer
        """
        rsp = None
        if item < 0:
            rsp = self.create_negint(item)
        else:
            rsp = self.create_posint(item)
        return rsp

    def create_negint(self,item):
        """
        Create a DollarItem from a negative integer
        """
        raw_value = item.to_bytes((item.bit_length() + 7) // 8, "little",signed=True)
        item_value = item
        lenght = self.get_meta_value_length(raw_value)
        buffer = lenght + Dollartype.ITEM_NEGINT.value.to_bytes(1, "little") + raw_value
        return DollarItem(
            dollar_type=Dollartype.ITEM_NEGINT.value,
            value=item_value,
            raw_value=raw_value,
            buffer=buffer
        )

    def create_posint(self,item):
        """
        Create a DollarItem from a positive integer
        """
        raw_value = item.to_bytes((item.bit_length() + 7) // 8, "little")
        item_value = item
        lenght = self.get_meta_value_length(raw_value)
        buffer = lenght + Dollartype.ITEM_POSINT.value.to_bytes(1, "little") + raw_value
        return DollarItem(
            dollar_type=Dollartype.ITEM_POSINT.value,
            value=item_value,
            raw_value=raw_value,
            buffer=buffer
        )

    def create_from_float(self,item):
        """
        Create a DollarItem from a float
        """
        rsp = None
        if item < 0:
            rsp = self.create_negnum(item)
        else:
            rsp = self.create_posnum(item)
        return rsp

    def create_negnum(self,item):
        """
        Create a DollarItem from a negative float
        """
        # convert the float to a positive interger with a scale
        # 1.2345 -> 12345 with scale 4

        # get the scale
        scale = len(str(item).split('.')[1]) * -1
        # convert to int
        num = int(item * (10 ** (scale * -1)))
        # create the item
        raw_value = scale.to_bytes(1, "little",signed=True)+num.to_bytes((num.bit_length() + 7) // 8, "little",signed=True)

        item_value = item
        lenght = self.get_meta_value_length(raw_value)
        buffer = lenght + Dollartype.ITEM_NEGNUM.value.to_bytes(1, "little") + raw_value
        return DollarItem(
            dollar_type=Dollartype.ITEM_NEGNUM.value,
            value=item_value,
            raw_value=raw_value,
            buffer=buffer
        )

    def create_posnum(self,item):
        """
        Create a DollarItem from a positive float
        """
        # convert the float to a positive interger with a scale
        # 1.2345 -> 12345 with scale 4

        # get the scale
        scale = len(str(item).split('.')[1]) * -1
        # convert to int
        num = int(item * (10 ** (scale * -1)))
        # create the item
        raw_value = scale.to_bytes(1, "little",signed=True)+num.to_bytes((num.bit_length() + 7) // 8, "little")

        item_value = item
        lenght = self.get_meta_value_length(raw_value)
        buffer = lenght + Dollartype.ITEM_POSNUM.value.to_bytes(1, "little") + raw_value
        return DollarItem(
            dollar_type=Dollartype.ITEM_POSNUM.value,
            value=item_value,
            raw_value=raw_value,
            buffer=buffer
        )

    def get_meta_value_length(self,raw_value):
        """
        Get the length of the raw value
        """
        response = b''
        length = len(raw_value) + 2
        # convert bit_length to bytes
        bytes_length = (length.bit_length() + 7) // 8

        if bytes_length == 1:
            response = length.to_bytes(1, "little")
        elif bytes_length == 2:
            response = b'\x00' + (length-1).to_bytes(2, "little")
        elif 2 < bytes_length < 5:
            response = b'\x00\x00\x00' + (length-1).to_bytes(4, "little")
        elif bytes_length > 4:
            raise DollarListException("Value is too long")
        return response

class DollarList:

    items: List[DollarItem] = []

    def __init__(self, value=None):
        if value is not None:
            if isinstance(value, bytes):
                for item in self.from_bytes(value):
                    self.items.append(item)
            elif isinstance(value, list):
                for item in self.from_list(value):
                    self.items.append(item)
            elif isinstance(value, str):
                for item in self.from_string(value):
                    self.items.append(item)
            elif isinstance(value, DollarList):
                for item in value.items:
                    self.items.append(item)
            else:
                raise DollarListException("Invalid value type")
        else:
            self.items = []

    def append(self,item):
        """
        Append a new item to the list
        """
        self.items.append(DollarListWriter().create_dollar_item(item))

    @staticmethod
    def from_string(string):
        """
        Create a DollarList from a string
        String input is in the format of:
        $lb(<item1>,<item2>,<item3>,<item4>...)
        where item can be:
        - a string
        - a number
        - a list
        A list can be nested
        Parse the string item by item. Move in the string until the next ',' or ')'
        """
        def parse_list(string):
            count = 0
            for i,value in enumerate(string):
                if string[i:i+4] == '$lb(':
                    count += 1
                elif value == ')':
                    count -= 1
                if count == 0:
                    item = DollarList.from_string(string[0:i+1])
                    return item,string[i+2:]
            raise DollarListException("Invalid string")

        def parse_item(string):
            for i,value in enumerate(string):
                if value in (',' , ')'):
                    if string[0] == '"':
                        item = DollarListWriter().create_dollar_item(string[1:i-1])
                    else:
                        item = DollarListWriter().create_dollar_item(int(string[0:i]))
                    return item,string[i+1:]
            raise DollarListException("Invalid string")

        if string[0:3] != '$lb':
            raise DollarListException("Invalid string format")
        string = string[3:]
        if string[0] != '(':
            raise DollarListException("Invalid string format")
        string = string[1:]
        response = DollarList()
        while len(string) > 0:
            if string[0] == '$':
                # list
                item, string = parse_list(string)
                response.append(item)
            else:
                # item
                item, string = parse_item(string)
                response.append(item)
        return response

    def __len__(self):
        return len(self.items)

    def to_bytes(self):
        """
        Convert a DollarList to bytes
        """
        buffer = b''
        for item in self.items:
            buffer += item.buffer
        return buffer

    @staticmethod
    def from_list(python_list):
        """
        Create a DollarListWriter from a python list
        For each item in the list, create a DollarItem
        """
        dollar_list = DollarList()
        if isinstance(python_list, list):
            if len(python_list) > 0:
                for item in python_list:
                    dollar_list.append(item)
            else:
                dollar_list.append(None)
        else:
            raise DollarListException("Invalid input type")
        return dollar_list

    # add to the dataclass a new constructor from_bytes
    @staticmethod
    def from_bytes(buffer:bytes):
        cls = DollarList()
        cls.items = DollarListReader(buffer).items
        return cls

    def __str__(self):
        """
        Return a string representation of the list.
        Like the dollar list representation with $lb
        """
        return self._str_(self.items)

    @classmethod
    def _str_(cls,items):
        """
        Return a string representation of the list.
        Like the dollar list representation with $lb"""
        response = "$lb("
        for item in items:

            if item.dollar_type in (Dollartype.ITEM_ASCII.value,
                                    Dollartype.ITEM_UNICODE.value):
                if item.value is None:
                    response += '""' # way of iris to represent null string
                else:
                    response += f'"{item.value}"'

            elif item.dollar_type == Dollartype.ITEM_PLACEHOLDER.value:
                response += cls._str_(item.value.items)
            else:
                response += f'{item.value}'
            response += ","
        if len(items) > 0:
            response = response[:-1]
        if len(items) == 0:
            response += '""'
        response += ")"
        return response

    @classmethod
    def _to_list(cls,items):
        """
        Convert a list of DollarItems to a list of python objects
        """
        response = []
        for item in items:
            if item.dollar_type == 0:
                response.append(cls._to_list(item.value))
            else:
                response.append(item.value)
        return response

    def to_list(self):
        """
        Convert a list of DollarItems to a list of python objects
        """
        return self._to_list(self.items)

    # build iterator for values
    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = DollarListWriter().create_dollar_item(value)

    def __delitem__(self, index):
        del self.items[index]

    def __contains__(self, item):
        return DollarListWriter().create_dollar_item(item) in self.items

    def __eq__(self, other):
        return self.items == other.items

    def __ne__(self, other):
        return self.items != other.items

    def __add__(self, other):
        result = self.items + other.items
        return DollarList(result)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.items)

    def __sizeof__(self):
        return len(self.items)
