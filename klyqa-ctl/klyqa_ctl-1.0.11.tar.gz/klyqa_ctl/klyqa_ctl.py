#!/usr/bin/env python3
"""Klyqa control client."""

###################################################################
#
# Interactive Klyqa Control commandline client
#
# Company: QConnex GmbH / Klyqa
# Author: Frederick Stallmeyer
#
# E-Mail: frederick.stallmeyer@gmx.de
#
# nice to haves:
#   -   list cloud connected devices in discovery.
#   -   offer for selected devices possible commands and arguments in interactive
#       mode based on their device profile
#   -   Implementation for the different device config profile versions and
#       check on send.
#
# BUGS:
#  - vc1 interactive command selection support.
#
###################################################################

from __future__ import annotations
from dataclasses import dataclass
import socket
import sys
import json
import datetime
import argparse
import select
import logging
from typing import TypeVar, Any, Type
from strenum import StrEnum

NoneType: Type[None] = type(None)
import requests, uuid, json
import os.path
from threading import Thread
from collections import ChainMap
from threading import Event
from enum import Enum
import asyncio, aiofiles
import functools, traceback
from asyncio.exceptions import CancelledError, TimeoutError
from collections.abc import Callable

import slugify as unicode_slug

try:
    from Cryptodome.Cipher import AES  # provided by pycryptodome
    from Cryptodome.Random import get_random_bytes  # pycryptodome
except:
    from Crypto.Cipher import AES  # provided by pycryptodome
    from Crypto.Random import get_random_bytes  # pycryptodome

from typing import TypeVar

# DEFAULT_SEND_TIMEOUT_MS=5000000000
DEFAULT_SEND_TIMEOUT_MS = 5000

LOGGER: logging.Logger = logging.getLogger(__package__)
LOGGER.setLevel(level=logging.INFO)
formatter: logging.Formatter = logging.Formatter("%(asctime)s %(levelname)-8s - %(message)s")

logging_hdl = logging.StreamHandler()
logging_hdl.setLevel(level=logging.INFO)
logging_hdl.setFormatter(formatter)

LOGGER.addHandler(logging_hdl)

s: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

print(f"{s} start")

TypeJSON = dict[str, Any]

""" string output separator width """
sep_width = 0

AES_KEY_DEV: bytes = bytes(
    [
        0x00,
        0x11,
        0x22,
        0x33,
        0x44,
        0x55,
        0x66,
        0x77,
        0x88,
        0x99,
        0xAA,
        0xBB,
        0xCC,
        0xDD,
        0xEE,
        0xFF,
    ]
)

## Bulbs ##

BULB_SCENES: list[dict[str, Any]] = [
    {
        "id": 100,
        "colors": ["#FFECD8", "#FFAA5B"],
        "label": "Warm White",
        "commands": "5ch 0 0 0 0 65535 65535 500;p 1000;",
        "cwww": True,
    },
    {
        "id": 101,
        "colors": ["#FCF4DD", "#FED07A"],
        "label": "Daylight",
        "commands": "5ch 0 0 0 24903 40631 65535 500;p 1000;",
    },
    {
        "id": 102,
        "colors": ["#FFFFFF", "#B6DAFF"],
        "label": "Cold White",
        "commands": "5ch 0 0 0 65535 0 65535 500;p 1000;",
        "cwww": True,
    },
    {
        "id": 103,
        "colors": ["#E06004", "#55230D"],
        "label": "Night Light",
        "commands": "5ch 9830 3276 0 1310 0 65535 500;p 1000;",
        "cwww": True,
    },
    {
        "id": 106,
        "colors": ["#FDCB78", "#FCDA60"],
        "label": "Relax",
        "commands": "5ch 26214 26214 0 0 13107 65535 500;p 1000;",
    },
    {
        "id": 109,
        "colors": ["#090064", "#2E2A5A"],
        "label": "TV Time",
        "commands": "5ch 655 0 6553 1310 0 65535 500;p 1000;",
    },
    {
        "id": 107,
        "colors": ["#FFD1A2", "#FFEDDA"],
        "label": "Comfort",
        "commands": "5ch 47185 0 0 18349 0 65535 500;p 1000;",
    },
    {
        "id": 108,
        "colors": ["#EAFCFF", "#81DFF0"],
        "label": "Focused",
        "commands": "5ch 0 0 26214 5000 0 65535 500;p 1000;",
        "cwww": True,
    },
    {
        "id": 110,
        "colors": ["#CD3700", "#CD0000", "#CD6600"],
        "label": "Fireplace",
        "commands": "5ch 32767 0 0 0 1500 65535 500;p 500;5ch 55535 200 0 0 2000 65535 500;p 500;",
        # '5ch 32767 0 0 0 1500 65535 500;p 500;5ch 55535 200 0 0 2000 65535 500;p 500;5ch 32767 30000 0 0 1500 65535 500;p 500;5ch 25535 20000 0 0 2000 65535 500;p 500;5ch 62767 0 0 0 1500 65535 500;p 500;5ch 65535 200 0 0 2000 65535 500;p 500;5ch 32767 30000 0 0 1500 65535 500;p 500;5ch 25535 30000 0 0 2000 65535 500;p 500;',
    },
    {
        "id": 122,
        "colors": ["#12126C", "#B22222", "#D02090"],
        "label": "Jazz Club",
        "commands": "5ch 45746 8738 8738 0 0 65535 6100;p 5100;5ch 45232 12336 24672 0 0 65535 6100;p 5000;5ch 53436 8224 37008 0 0 65535 6100;p 5000;5ch 0 0 33896 0 0 65535 6000;p 5000;5ch 18504 15677 35728 0 0 65535 6100;p 5000;5ch 38036 0 52428 0 0 65535 6600;p 5000;5ch 45232 12336 24672 0 0 65535 6100;p 5000;",
    },
    {
        "id": 104,
        "colors": ["#B20C26", "#CC1933", "#EE6AA7"],
        "label": "Romantic",
        "commands": "5ch 58981 6553 16383 0 0 65535 1000;p 7400;5ch 45874 3276 9830 0 0 65535 4400;p 6600;5ch 52428 6553 13107 0 0 65535 8800;p 15200;5ch 41287 0 0 0 0 65535 4400;p 13200;",
    },
    {
        "id": 112,
        "colors": ["#FFDCE8", "#D2FFD2", "#CCFFFF"],
        "label": "Gentle",
        "commands": "5ch 51117 0 0 13107 0 65535 26000;p 56000;5ch 26214 26214 0 8519 0 65535 26000;p 56000;5ch 0 51117 0 13107 0 65535 26000;p 56000;5ch 0 26214 26214 8519 0 65535 26000;p 56000;5ch 0 0 51117 13107 0 65535 26000;p 56000;5ch 26214 0 26214 8519 0 65535 26000;p 56000;",
    },
    {
        "id": 113,
        "colors": ["#EEAD0E", "#FF7F24", "#CD0000"],
        "label": "Summer",
        "commands": "5ch 17039 25558 0 13762 0 65535 8000;p 14000;5ch 39321 7864 0 15728 0 65535 8000;p 14000;5ch 28180 17694 0 11140 0 65535 8000;p 14000;",
    },
    {
        "id": 114,
        "colors": ["#00BA0C", "#008400", "#0C4400"],
        "label": "Jungle",
        "commands": "5ch 0 47840 3276 0 0 65535 2600;p 2100;5ch 5898 10485 1310 0 0 65535 2300;p 4200;5ch 0 34078 0 0 0 65535 2100;p 2500;5ch 3276 17694 0 0 0 65535 4600;p 4000;5ch 9174 46529 0 0 0 65535 5500;p 6900;5ch 9830 43908 1966 0 0 65535 2700;p 4700;5ch 0 55704 0 0 0 65535 2000;p 3800;",
    },
    {
        "id": 105,
        "colors": ["#00008B", "#0000FF", "#1874ED"],
        "label": "Ocean",
        "commands": "5ch 1310 17694 36044 0 0 65535 2400;p 5400;5ch 655 15073 39321 0 0 65535 2100;p 5100;5ch 1310 36044 17039 0 0 65535 4200;p 5100;5ch 1966 22281 29490 0 0 65535 2800;p 5700;5ch 655 19005 34733 0 0 65535 2100;p 4900;5ch 655 26869 27524 0 0 65535 2600;p 3400;5ch 655 26869 27524 0 0 65535 2700;p 3600;5ch 1310 38010 15728 0 0 65535 4200;p 5000;",
    },
    # {
    #   "id": 111,
    #   "colors": ['#A31900', '#A52300', '#B71933', '#A5237F', '#B71900'],
    #   "label": 'Club',
    #   "commands":
    #     '5ch 41942 6553 0 1310 0 65535 600;p 800;5ch 42597 9174 0 1310 0 65535 8700;p 12000;5ch 47185 6553 13107 1310 0 65535 8700;p 12000;5ch 42597 9174 32767 1310 0 65535 300;p 400;5ch 47185 6553 0 1310 0 65535 300;p 1300;',
    # },
    {
        "id": 115,
        "colors": ["#EE4000", "#CD6600", "#FFA500"],
        "label": "Fall",
        "commands": "5ch 49151 1966 0 9830 0 65535 8400;p 8610;5ch 35388 13107 0 6553 0 65535 8400;p 8750;5ch 52428 0 0 10485 0 65535 8400;p 8740;5ch 39321 9174 0 12451 0 65535 500;p 840;",
    },
    {
        "id": 116,
        "colors": ["#FFF0F5", "#FF6EB4", "#FF4500"],
        "label": "Sunset",
        "commands": "5ch 39321 0 15073 2621 0 65535 5680;p 5880;5ch 51117 0 0 13107 0 65535 5680;p 5880;5ch 43253 11796 0 2621 0 65535 5680;p 5880;5ch 38010 0 15073 7208 0 65535 5680;p 5880;5ch 46529 0 0 3932 0 65535 5680;p 5880;5ch 41287 11140 0 7864 0 65535 5680;p 5880;",
    },
    {
        "id": 117,
        "colors": ["#FF0000", "#0000FF", "#00FF00"],
        "label": "Party",
        "commands": "5ch 55704 0 0 0 0 65535 132;p 272;5ch 55704 0 0 0 0 65535 132;p 272;5ch 0 55704 0 0 0 65535 132;p 272;5ch 0 55704 0 0 0 65535 132;p 272;5ch 0 0 55704 0 0 65535 132;p 272;5ch 0 0 55704 0 0 65535 132;p 272;5ch 28180 0 27524 0 0 65535 132;p 272;5ch 0 28180 27524 0 0 65535 132;p 272;",
    },
    {
        "id": 118,
        "colors": ["#F0FFF0", "#C1FFC1", "#FFE4E1"],
        "label": "Spring",
        "commands": "5ch 19660 15728 19660 0 0 65535 8000;p 11000;5ch 20315 26214 13107 0 0 65535 8000;p 11000;5ch 17039 19005 19005 0 0 65535 8000;p 11000;5ch 20315 14417 14417 0 0 65535 8000;p 11000;5ch 19005 18349 17694 0 0 65535 8000;p 11000;5ch 11796 30146 6553 0 0 65535 8000;p 11000;",
    },
    {
        "id": 119,
        "colors": ["#C1FFC1", "#C0FF3E", "#CAFF70"],
        "label": "Forest",
        "commands": "5ch 23592 22937 0 3932 0 65535 6000;p 8000;5ch 19005 23592 0 7864 0 65535 6200;p 10100;5ch 22281 21626 0 12451 0 65535 6000;p 10000;5ch 23592 22281 0 4587 0 65535 5800;p 10400;5ch 18349 27524 0 1966 0 65535 6200;p 7000;5ch 8519 25558 0 23592 0 65535 6200;p 9400;",
    },
    {
        "id": 120,
        "colors": ["#104E8B", "#00008B", "#4876FF"],
        "label": "Deep Sea",
        "commands": "5ch 3932 3276 59636 0 0 65535 4100;p 5100;5ch 3276 6553 53738 0 0 65535 4100;p 5000;5ch 0 0 43908 0 0 65535 4100;p 5000;5ch 655 1310 53083 0 0 65535 3600;p 5000;5ch 1310 0 53738 0 0 65535 4000;p 5000;",
    },
    {
        "id": 121,
        "colors": ["#90ee90", "#8DEEEE", "#008B45"],
        "label": "Tropical",
        "commands": "5ch 0 43253 0 0 36044 65535 3000;p 4000;5ch 0 0 0 0 65535 65535 2400;p 5400;5ch 0 38010 0 0 48495 65535 2600;p 3600;5ch 0 32767 0 0 0 65535 2000;p 3400;5ch 0 46529 0 0 26869 65535 3100;p 4100;5ch 0 43908 0 0 0 65535 4000;p 7000;5ch 0 49806 0 0 16383 65535 2000;p 5000;",
    },
    {
        "id": 123,
        "colors": ["#FF6AD0", "#8BFFC7", "#96A0FF"],
        "label": "Magic Mood",
        "commands": "5ch 65535 27242 53456 0 0 35535 2400;p 1180;5ch 30326 33924 65535 0 0 35535 2200;p 1110;5ch 65535 21331 21331 0 0 35535 2800;p 1200;5ch 35723 55535 31143 0 0 35535 2800;p 1200;5ch 38550 41120 65535 0 0 35535 2400;p 1040;5ch 65535 61423 29041 0 0 35535 2400;p 1000;",
    },
    {
        "id": 124,
        "colors": ["#FF0000", "#B953FF", "#DBFF96"],
        "label": "Mystic Mountain",
        "commands": "5ch 65535 0 0 0 0 35535 1400;p 980;5ch 65535 30326 52685 0 0 35535 1200;p 910;5ch 47543 21331 65535 0 0 35535 1800;p 1200;5ch 35723 65535 44461 0 0 35535 1800;p 1200;5ch 56283 65535 38550 0 0 35535 1400;p 1040;5ch 65535 29041 53456 0 0 35535 1400;p 1000;",
    },
    {
        "id": 125,
        "colors": ["#FB0000", "#FFF748", "#B97FFF"],
        "label": "Cotton Candy",
        "commands": "5ch 65535 0 52428 0 0 35535 1400;p 980;5ch 47545 32639 655350 0 0 35535 1200;p 910;5ch 65535 33410 33410 0 0 35535 1800;p 1200;5ch 65535 63479 18504 0 0 35535 1800;p 1200;5ch 65535 63222 16448 0 0 35535 1400;p 1040;5ch 64507 0 0 0 0 35535 1400;p 1000;",
    },
    {
        "id": 126,
        "colors": ["#8BFFE1", "#D8FA97", "#FF927F"],
        "label": "Ice Cream",
        "commands": "5ch 65535 0 0 0 0 35535 1400;p 980;5ch 65535 37522 32639 0 0 35535 1200;p 910;5ch 61166 54741 65535 0 0 35535 1800;p 1200;5ch 35723 65535 57825 0 0 35535 1800;p 1200;5ch 55512 64250 38807 0 0 35535 1400;p 1040;5ch 65535 56796 62709 0 0 35535 1400;p 1000;",
    },
]

## Vacuum Cleaner ##

VC_WORKINGSTATUS: Type[Enum] = Enum(
    "VC_WORKINGSTATUS",
    "SLEEP STANDBY CLEANING CLEANING_AUTO CLEANING_RANDOM CLEANING_SROOM CLEANING_EDGE CLEANING_SPOT CLEANING_COMP DOCKING CHARGING CHARGING_DC CHARGING_COMP ERROR",
)

VC_SUCTION_STRENGTHS: Type[Enum] = Enum(
    "VC_SUCTION_STRENGTHS",
    "NULL STRONG SMALL NORMAL MAX",
)

VC_WORKINGMODE: Type[Enum] = Enum(
    "VC_WORKINGMODE",
    "STANDBY RANDOM SMART WALL_FOLLOW MOP SPIRAL PARTIAL_BOW SROOM CHARGE_GO"
)

class AsyncIOLock:
    """AsyncIOLock"""

    task: asyncio.Task
    lock: asyncio.Lock
    _instance = None

    def __init__(self) -> None:
        """__init__"""
        self.lock = asyncio.Lock()
        self.task = None

    async def acquire(self) -> None:
        """acquire"""
        await self.lock.acquire()
        self.task = asyncio.current_task()

    def release(self) -> None:
        """release"""
        self.lock.release()

    def force_unlock(self) -> bool:
        """force_unlock"""
        try:
            self.task.cancel()
            self.lock.release()
        except:
            return False
        return True

    @classmethod
    def instance(
        cls,
    ):
        """instance"""
        if cls._instance is None:
            LOGGER.debug("Creating new AsyncIOLock instance")
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._instance.__init__()
        return cls._instance


tcp_udp_port_lock: AsyncIOLock = AsyncIOLock.instance()


class RefParse:
    """RefParse"""

    ref = None

    def __init__(self, ref) -> None:
        self.ref = ref


async def async_json_cache(json_data, json_file) -> tuple [Device_config, bool]:
    """
    If json data is given write it to cache json_file.
    Else try to read from json_file the cache.
    """

    return_json: Device_config = json_data
    cached = False
    if json_data:
        """
        save the json for offline cache in dirpath where called script resides
        ids: { sets }
        """
        return_json = json_data
        try:
            s = ""
            for id, sets in json_data.items():
                if isinstance(sets, (datetime.datetime, datetime.date)):
                    sets = sets.isoformat()
                s = s + '"' + id + '": ' + json.dumps(sets) + ", "
            s = "{" + s[:-2] + "}"
            async with aiofiles.open(
                os.path.dirname(sys.argv[0]) + f"/{json_file}", mode="w"
            ) as f:
                await f.write(s)
        except Exception as e:
            LOGGER.warning(f'Could not save cache for json file "{json_file}".')
    else:
        """no json data, take cached json from disk if available"""
        try:
            async with aiofiles.open(
                os.path.dirname(sys.argv[0]) + f"/{json_file}", mode="r"
            ) as f:
                s = await f.read()
            return_json = json.loads(s)
            cached = True
        except:
            LOGGER.warning(f'No cache from json file "{json_file}" available.')
    return (return_json, cached)


def get_fields(object):
    """get_fields"""
    if hasattr(object, "__dict__"):
        return object.__dict__.keys()
    else:
        return dir(object)


def get_obj_attrs_as_string(object) -> str:
    """get_obj_attrs_as_string"""
    fields = get_fields(object)
    attrs = [
        a for a in fields if not a.startswith("__") and not callable(getattr(object, a))
    ]
    return ", ".join(attrs)


def get_obj_attr_values_as_string(object) -> str:
    """get_obj_attr_values_as_string"""
    fields = get_fields(object)
    attrs = [
        a for a in fields if not a.startswith("__") and not callable(getattr(object, a))
    ]
    vals = []
    for a in attrs:
        _str: str = str(getattr(object, a))
        vals.append(_str if _str else '""')
    return ", ".join(vals)


class RGBColor:
    """RGBColor"""

    r: int
    g: int
    b: int

    def __str__(self) -> str:
        return "[" + ",".join([str(self.r), str(self.g), str(self.b)]) + "]"
        # return get_obj_values_as_string(self)

    def __init__(self, r: int, g: int, b: int) -> None:
        self.r = r
        self.g = g
        self.b = b


def format_uid(text: str) -> str:
    return unicode_slug.slugify(text)

class KlyqaDeviceResponse:
    # type: str = ""

    def __init__(
        self,
        # type: str,
        **kwargs) -> None:
        """__init__"""
        self.type: str = ""
        self.ts: datetime.datetime = datetime.datetime.now()
        self.update(**kwargs)

    def update(self, **kwargs) -> None:
        # Walk through parsed kwargs dict and look if names in dict exists as attribute in class,
        # then apply the value in kwargs to the value in class.
        for attr in kwargs:
            if hasattr(self, attr):
                setattr(self, attr, kwargs[attr])

# class KlyqaDeviceResponse:
#     """KlyqaDeviceResponse"""

#     type: str = ""
#     response_msg: dict = {}
#     ts: datetime.datetime = datetime.datetime.now()

#     def __init__(self, type=type, response_msg: dict = {}) -> None:
#         self.type = type
#         self.response_msg = response_msg
#         self.ts = datetime.datetime.now()


# eventually dataclass
class KlyqaDeviceResponseIdent(KlyqaDeviceResponse):
    """KlyqaDeviceResponseIdent"""

    def __init__(
        self,
        **kwargs,
    ) -> None:
        self.fw_version: str = ""
        self.fw_build: str = ""
        self.hw_version: str = ""
        self.manufacturer_id: str = ""
        self.product_id: str = ""
        self.sdk_version: str = ""
        self._unit_id: str = ""
        super().__init__(**kwargs)

    def update(self, **kwargs) -> None:
        super().update(**kwargs)

    @property
    def unit_id(self) -> str:
        return self._unit_id

    @unit_id.setter
    def unit_id(self, unit_id: str) -> None:
        self._unit_id = format_uid(unit_id)

class KlyqaVCResponseStatus(KlyqaDeviceResponse):
    """KlyqaVCResponseStatus"""

# Decrypted:  b'{"type":"statechange","mcu":"online","power":"on",
# "cleaning":"on","beeping":"off","battery":57,"sidebrush":10,
# "rollingbrush":30,"filter":60,"carpetbooster":200,"area":999,
# "time":999,"calibrationtime":19999999,"workingmode":null,
# "workingstatus":"STANDBY","suction":"MID","water":"LOW","direction":"STOP",
# "errors":["COLLISION","GROUND_CHECK","LEFT_WHEEL","RIGHT_WHEEL","SIDE_SCAN","MID_SWEEP","FAN","TRASH","BATTERY","ISSUES"],
# "cleaningrec":[],"equipmentmodel":"","alarmmessages":"","commissioninfo":"","action":"get"}

    def __str__(self) -> str:
        """__str__"""
        return get_obj_attr_values_as_string(self)

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """__init__"""
        self.action: str = ""
        self.active_command: int = -1
        self.alarmmessages: str = ""
        self.area: int = -1
        self.beeping: str = ""
        self.battery: str = ""
        self.calibrationtime: int = -1
        self.carpetbooster: int = -1
        self.cleaning: str = ""
        self.cleaningrec: list[str] = []
        self.connected: bool = False
        self.commissioninfo: str = ""
        self.direction: str = ""
        self.errors: list[str] = []
        self.equipmentmodel: str = ""
        self.filter: int = -1
        self.filter_tresh: int = -1
        self.fwversion: str = ""
        self.id: str = ""
        self.lastActivityTime: str = ""
        self.map_parameter: str = ""
        self.mcuversion: str = ""
        self.open_slots: int = -1
        self.power: str = ""
        self.rollingbrush_tresh: int = -1
        self.rollingbrush: int = -1
        self.sdkversion: str = ""
        self.sidebrush: str = ""
        self.sidebrush_tresh: int = -1
        self.suction: str = ""
        self.time: int = -1
        self.ts: datetime.datetime = datetime.datetime.now()
        self.watertank: str = ""
        self.workingmode: str | None = None
        self.workingstatus: str = ""

        LOGGER.debug(f"save status {self}")
        super().__init__(**kwargs)

    def update(self, **kwargs) -> None:
        super().update(**kwargs)

class KlyqaBulbResponseStatus(KlyqaDeviceResponse):
    """Klyqa_Bulb_Response_Status"""

    # status: str = ""
    # color: RGBColor = RGBColor(-1, -1, -1)
    # brightness: int = -1
    # temperature: int = -1
    # active_command: int = -1
    # active_scene: str = ""
    # open_slots: int
    # mode: str = ""
    # fwversion: str = ""
    # sdkversion: str = ""
    # ts: datetime.datetime = datetime.datetime.now()

    def __str__(self) -> str:
        """__str__"""
        return get_obj_attr_values_as_string(self)

    def __init__(
        self,
        # type: str,
        # status: str = "off",
        # brightness: dict[str, int] = {},
        # mode: str = "",
        # open_slots: int = 0,
        # fwversion: str = "",
        # sdkversion: str = "",
        # color: dict[str, int] = {},
        # temperature: int = -1,
        # active_command: int = 0,
        # active_scene: str = 0,
        **kwargs
    ) -> None:
        """__init__"""
        # self.status = status
        # self.color = (
        #     RGBColor(color["red"], color["green"], color["blue"]) if color else {}
        # )
        # self.brightness = brightness["percentage"] if brightness else 0
        # self.temperature = temperature
        # self.active_command = active_command
        # self.active_scene = active_scene
        # self.open_slots = open_slots
        # self.mode = mode
        # self.fwversion = fwversion
        # self.sdkversion = sdkversion
        self.active_command: int | None = None
        self.active_scene: str | None = None
        self._brightness: int | None = None
        self._color: RGBColor | None = None
        self.fwversion: str | None = None
        self.mode: str | None = None # cmd, cct, rgb
        self.open_slots: int | None = None
        self.sdkversion: str | None = None
        self.status: str | None = None
        self.temperature: int | None = None
        LOGGER.debug(f"save status {self}")
        super().__init__(**kwargs)

    @property
    def brightness(self) -> int:
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: dict[str, int]):
        self._brightness = int(brightness["percentage"])

    @property
    def color(self) -> RGBColor | None:
        return self._color

    @color.setter
    def color(self, color: dict[str, int]):
        self._color = RGBColor(color["red"], color["green"], color["blue"]) if color else None


Device_config = dict

device_configs: dict[str, Device_config] = dict()


class LocalConnection:
    """LocalConnection"""

    state: str = "WAIT_IV"
    localIv: bytes = get_random_bytes(8)
    remoteIv: bytes = b""

    sendingAES: bytes = None
    receivingAES: bytes = None
    address: dict[str, Any] = {"ip": "", "port": -1}
    connection: socket.socket = None
    received_packages = []
    sent_msg_answer = {}
    aes_key_confirmed: bool = False

    def __init__(self) -> None:
        self.state = "WAIT_IV"
        self.localIv = get_random_bytes(8)

        self.sendingAES = None
        self.receivingAES = None
        self.address = {"ip": "", "port": -1}
        self.connection: socket.socket = None
        self.received_packages = []
        self.sent_msg_answer = {}
        self.aes_key_confirmed = False


class CloudConnection:
    """CloudConnection"""

    received_packages = []
    connected: bool

    def __init__(self) -> None:
        self.connected = False
        self.received_packages = []


Device_TCP_return: Type[Device_TCP_return] = Enum(
    "Device_TCP_return",
    "sent answered wrong_uid wrong_aes tcp_error unknown_error timeout nothing_done sent_error no_message_to_send device_lock_timeout err_local_iv missing_aes_key response_error",
)


Message_state: Type[Message_state] = Enum("Message_state", "sent answered unsent")


@dataclass
class Message:
    started: datetime.datetime
    msg_queue: list[tuple]
    msg_queue_sent = []  #: list[str] = dataclasses.field(default_factory=list)
    args: list[str]
    target_uid: str
    state: Message_state = Message_state.unsent
    finished: datetime.datetime = None
    answer: str = ""
    answer_utf8: str = ""
    answer_json = {}
    # callback on error event or answer
    callback: Callable[[Any], None] = NoneType
    time_to_live_secs: int = -1
    msg_counter: int = -1

    def __post_init__(self) -> None:
        # super().__init__(self, *args, **kwargs)
        global MSG_COUNTER
        self.msg_counter = MSG_COUNTER
        MSG_COUNTER = MSG_COUNTER + 1

    async def call_cb(self) -> None:
        await self.callback(self, self.target_uid)

    async def check_msg_ttl(self) -> bool:
        if datetime.datetime.now() - self.started > datetime.timedelta(
            seconds=self.time_to_live_secs
        ):
            LOGGER.debug(
                f"time to live {self.time_to_live_secs} seconds for message {self.msg_counter} {self.msg_queue} ended."
            )
            if self.callback:
                await self.call_cb()
            return False
        return True

class KlyqaDevice:
    """KlyqaDevice"""

    local: LocalConnection
    cloud: CloudConnection

    u_id: str = "no_uid"
    acc_sets: dict = {}
    """ account settings """

    _use_lock: asyncio.Lock
    _use_thread: asyncio.Task

    recv_msg_unproc: list[Message]
    ident: KlyqaDeviceResponseIdent = None

    response_classes = {}
    status: KlyqaDeviceResponse | None

    def __init__(self) -> None:
        self.local = LocalConnection()
        self.cloud = CloudConnection()
        self.ident: KlyqaDeviceResponseIdent = KlyqaDeviceResponseIdent()

        self.u_id: str = "no_uid"
        self.acc_sets = {}
        self._use_lock = None
        self._use_thread = None
        self.recv_msg_unproc = []

        self.status = None
        self.response_classes = {
            "ident": KlyqaDeviceResponseIdent,
            "status": KlyqaDeviceResponse,
        }

    def process_msgs(self) -> None:
        for msg in self.recv_msg_unproc:
            LOGGER.debug(f"updating device {self.u_id} entity with msg:")
            self.recv_msg_unproc.remove(msg)

    def get_name(self) -> str:
        return (
            f"{self.acc_sets['name']} ({self.u_id})"
            if self.acc_sets and "name" in self.acc_sets and self.acc_sets
            else self.u_id
        )

    async def use_lock(self, timeout=30, **kwargs) -> bool:
        try:
            if not self._use_lock:
                self._use_lock = asyncio.Lock()

            LOGGER.debug(f"wait for lock... {self.get_name()}")

            if await self._use_lock.acquire():
                self._use_thread = asyncio.current_task()
                LOGGER.debug(f"got lock... {self.get_name()}")
                return True
        except asyncio.TimeoutError:
            LOGGER.error(f'Timeout for getting the lock for device "{self.get_name()}"')
        except Exception as excp:
            LOGGER.debug(f"different error while trying to lock.")

        return False

    async def use_unlock(self) -> None:
        if not self._use_lock:
            self._use_lock = asyncio.Lock()
        if self._use_lock.locked() and self._use_thread == asyncio.current_task():
            try:
                self._use_lock.release()
                self._use_thread = None
                LOGGER.debug(f"got unlock... {self.get_name()}")
            except:
                pass

    def save_device_message(self, msg) -> None:
        """msg: json dict"""

        status_update_types: set={"status", "statechange"}
        if msg["type"] in status_update_types:
            msg["type"] = "status"
        if "type" in msg and hasattr(self, msg["type"]): #and msg["type"] in msg:
            try:
                LOGGER.debug(f"save device msg {msg} {self.ident} {self.u_id}")
                if msg["type"] == "ident":
                    # setattr(self, "ident", self.ident.update(**msg))
                    # setattr(
                    #     self,
                    #     msg["type"],
                    #     self.response_classes[msg["type"]](**msg[msg["type"]]),
                    # )
                    self.ident.update(**msg["ident"])
                elif msg["type"] in status_update_types: # and self.status:
                    # setattr(self, msg["type"], self.response_classes[msg["type"]](**msg))
                    # setattr(self, "status", self.status.update(**msg))
                    if self.status is None:
                        self.status = self.response_classes["status"](**msg)
                    else:
                        self.status.update(**msg)
            except Exception as e:
                LOGGER.error(f"{traceback.format_exc()}")
                LOGGER.error("Could not process device response: ")
                LOGGER.error(str(msg))

class KlyqaVC(KlyqaDevice):
    """Klyqa vaccum cleaner"""

    # status: KlyqaVCResponseStatus = None

    def __init__(self) -> None:
        super().__init__()
        # self.status = KlyqaVCResponseStatus()
        self.response_classes["status"] = KlyqaVCResponseStatus

class KlyqaBulb(KlyqaDevice):
    """KlyqaBulb"""

    # status: KlyqaBulbResponseStatus = None

    def __init__(self) -> None:
        super().__init__()
        # self.status = KlyqaBulbResponseStatus()
        self.response_classes["status"] = KlyqaBulbResponseStatus

    def setTemp(self, temp: int):
        temperature_enum = []
        try:
            temperature_enum = [
                trait["value_schema"]["properties"]["colorTemperature"]["enum"]
                for trait in device_configs[self.ident.product_id]["deviceTraits"]
                if trait["trait"] == "@core/traits/color-temperature"
            ]
            if len(temperature_enum) < 2:
                raise Exception()
        except:
            LOGGER.error("No temperature change on the bulb available")
            return False
        if temp < temperature_enum[0] or temp > temperature_enum[1]:
            LOGGER.error(
                "Temperature for bulb out of range ["
                + temperature_enum[0]
                + ", "
                + temperature_enum[1]
                + "]."
            )
            return False


ReturnTuple = TypeVar("ReturnTuple", tuple[int, str], tuple[int, dict])


def send_msg(msg, device: KlyqaDevice):
    info_str: str = (
        'Sending in local network to "'
        + device.get_name()
        + '": '
        + json.dumps(json.loads(msg), sort_keys=True, indent=4)
    )

    LOGGER.info(info_str)
    plain = msg.encode("utf-8")
    while len(plain) % 16:
        plain = plain + bytes([0x20])

    cipher = device.local.sendingAES.encrypt(plain)

    while True:
        try:
            device.local.connection.send(
                bytes([len(cipher) // 256, len(cipher) % 256, 0, 2]) + cipher
            )
            return True
        except socket.timeout:
            LOGGER.debug("Send timed out, retrying...")
            pass
    return False


def color_message(red, green, blue, transition, skipWait=False) -> tuple[str, int]:
    waitTime = transition if not skipWait else 0
    return (
        json.dumps(
            {
                "type": "request",
                "color": {
                    "red": red,
                    "green": green,
                    "blue": blue,
                },
                "transitionTime": transition,
            }
        ),
        waitTime,
    )


def temperature_message(temperature, transition, skipWait=False) -> tuple[str, int]:
    waitTime = transition if not skipWait else 0
    return (
        json.dumps(
            {
                "type": "request",
                "temperature": temperature,
                "transitionTime": transition,
            }
        ),
        waitTime,
    )


def percent_color_message(red, green, blue, warm, cold, transition, skipWait) -> tuple[str, int]:
    waitTime = transition if not skipWait else 0
    return (
        json.dumps(
            {
                "type": "request",
                "p_color": {
                    "red": red,
                    "green": green,
                    "blue": blue,
                    "warm": warm,
                    "cold": cold,
                    # "brightness" : brightness
                },
                "transitionTime": transition,
            }
        ),
        waitTime,
    )


def brightness_message(brightness, transition) -> tuple[str, int]:
    return (
        json.dumps(
            {
                "type": "request",
                "brightness": {
                    "percentage": brightness,
                },
                "transitionTime": transition,
            }
        ),
        transition,
    )


AES_KEYs: dict[str, bytes] = {}


PRODUCT_URLS: dict[str, str] = {
    """TODO: Make permalinks for urls."""
    "@klyqa.lighting.cw-ww.gu10": "https://klyqa.de/produkte/gu10-white-strahler",
    "@klyqa.lighting.rgb-cw-ww.gu10": "https://klyqa.de/produkte/gu10-color-strahler",
    "@klyqa.lighting.cw-ww.g95": "https://www.klyqa.de/produkte/g95-vintage-lampe",
    "@klyqa.lighting.rgb-cw-ww.e14": "https://klyqa.de/produkte/e14-color-lampe",
    "@klyqa.lighting.cw-ww.e14": "https://klyqa.de/produkte/gu10-white-strahler",
    "@klyqa.lighting.rgb-cw-ww.e27": "https://www.klyqa.de/produkte/e27-color-lampe",
    "@klyqa.lighting.cw-ww.e27": "https://klyqa.de/produkte/e27-white-lampe",
    "@klyqa.cleaning.vc1": "https://klyqa.de/Alle-Produkte/Smarter-Starter",
}

commands_send_to_bulb: list[str] = [
    "request",
    "ping",
    "color",
    "temperature",
    "brightness",
    "routine_list",
    "routine_put",
    "routine_id",
    "routine_commands",
    "routine_delete",
    "routine_start",
    "power",
    "reboot",
    "factory_reset",
    "WW",
    "daylight",
    "CW",
    "nightlight",
    "relax",
    "TVtime",
    "comfort",
    "focused",
    "fireplace",
    "club",
    "romantic",
    "gentle",
    "summer",
    "jungle",
    "ocean",
    "fall",
    "sunset",
    "party",
    "spring",
    "forest",
    "deep_sea",
    "tropical",
    "magic",
    "mystic",
    "cotton",
    "ice",
    "command"
]

S = TypeVar("S", argparse.ArgumentParser, type(None))


class EventQueuePrinter:
    """Single event queue printer for job printing."""

    event: Event = Event()
    """event for the printer that new data is available"""
    not_finished: bool = True
    print_strings = []
    printer_t: Thread = None

    def __init__(self) -> None:
        """start printing helper thread routine"""
        self.printer_t = Thread(target=self.coroutine)
        self.printer_t.start()

    def stop(self) -> None:
        """stop printing helper thread"""
        self.not_finished = False
        self.event.set()
        self.printer_t.join(timeout=5)

    def coroutine(self) -> None:
        """printer thread routine, waits for data to print and/or a trigger event"""
        while self.not_finished:
            if not self.print_strings:
                self.event.wait()
            while self.print_strings and (l_str := self.print_strings.pop(0)):
                print(l_str, flush=True)

    def print(self, str) -> None:
        """add string to the printer"""
        self.print_strings.append(str)
        self.event.set()


def get_description_parser() -> argparse.ArgumentParser:
    """Make an argument parse object."""

    parser: ArgumentParser = argparse.ArgumentParser(
        description="Interactive klyqa device client (local/cloud). In default the client script tries to send the commands via local connection. Therefore a broadcast on udp port 2222 for discovering the lamps is sent in the local network. When the lamp receives the broadcast it answers via tcp on socket 3333 with a new socket tcp connection. On that tcp connection the commands are sent and the replies are received. "
    )

    return parser


def add_config_args(parser) -> None:
    """Add arguments to the argument parser object.

    Args:
        parser: Parser object
    """
    parser.add_argument(
        "--transitionTime", nargs=1, help="transition time in milliseconds", default=[0]
    )

    parser.add_argument("--myip", nargs=1, help="specify own IP for broadcast sender")

    # parser.add_argument(
    #     "--rerun",
    #     help="keep rerunning command",
    #     action="store_const",
    #     const=True,
    #     default=False,
    # )

    parser.add_argument(
        "--passive",
        help="vApp will passively listen vor UDP SYN from devices",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument("--aes", nargs=1, help="give aes key for the lamp")
    parser.add_argument("--username", nargs=1, help="give your username")
    parser.add_argument("--password", nargs=1, help="give your klyqa password")
    parser.add_argument(
        "--device_name",
        nargs=1,
        help="give the name of the device from your account settings for the command to send to",
    )
    parser.add_argument(
        "--device_unitids",
        nargs=1,
        help="give the device unit id from your account settings for the command to send to",
    )
    parser.add_argument(
        "--allDevices",
        help="send commands to all devices",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--discover",
        help="discover lamps",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--debug",
        help="Enable debug logging messages.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--selectDevice",
        help="Select device.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--force",
        help="If no configs (profiles) about the device available, send the command anyway (can be dangerous).",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--test",
        help="Test host server.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--prod",
        help="Production host server.",
        action="store_const",
        const=True,
        default=True,
    )
    parser.add_argument(
        "--local",
        help="Local connection to the devices only.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--cloud",
        help="Cloud connection to the devices only.",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--tryLocalThanCloud",
        help="Try local if fails then cloud connection to the devices. [This is default behaviour]",
        action="store_const",
        const=True,
        default=True,
    )
    parser.add_argument(
        "--dev",
        help="Developing mode. Use development AES key.",
        action="store_const",
        const=True,
        default=False,
    )


def add_command_args(parser):
    """Add arguments to the argument parser object.

    Args:
        parser: Parser object
    """
    parser.add_argument("--color", nargs=3, help="set color command (r,g,b) 0-255")
    parser.add_argument(
        "--temperature",
        nargs=1,
        help="set temperature command (kelvin range depends on lamp profile) (lower: warm, higher: cold)",
    )
    parser.add_argument("--brightness", nargs=1, help="set brightness in percent 0-100")
    parser.add_argument(
        "--percent_color",
        nargs=5,
        metavar=("RED", "GREEN", "BLUE", "WARM", "COLD"),
        help="set colors and white tones in percent 0 - 100",
    )
    parser.add_argument("--ota", nargs=1, help="specify http URL for ota")
    parser.add_argument(
        "--ping", help="send ping", action="store_const", const=True, default=False
    )
    parser.add_argument(
        "--request",
        help="send status request",
        action="store_const",
        const=True,
        default=False,
    )

    # TODO: currently not fully implemented
    # parser.add_argument(
    #     "--identity",
    #     help="send status request",
    #     action="store_const",
    #     const=True,
    #     default=False,
    # )

    parser.add_argument(
        "--factory_reset",
        help="trigger a factory reset on the device (Warning: device has to be onboarded again afterwards)",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--routine_list",
        help="lists stored routines",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--routine_put",
        help="store new routine",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--routine_delete",
        help="delete routine",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--routine_start",
        help="start routine",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--routine_id", help="specify routine id to act on (for put, start, delete)"
    )
    parser.add_argument("--routine_scene", help="specify routine scene label (for put)")
    parser.add_argument("--routine_commands", help="specify routine program (for put)")
    parser.add_argument(
        "--reboot",
        help="trigger a reboot",
        action="store_const",
        const=True,
        default=False,
    )
    parser.add_argument(
        "--power", nargs=1, metavar='"on"/"off"', help="turns the bulb on/off"
    )
    parser.add_argument(
        "--enable_tb", nargs=1, help="enable thingsboard connection (yes/no)"
    )

    parser.add_argument(
        "--fade", nargs=2, help="fade in/out time in milliseconds on powering device on/off", metavar=("IN", "OUT")
    )

    # parser.add_argument("--loop", help="loop", action="store_true")
    parser.add_argument("--WW", help="Warm White", action="store_true")
    parser.add_argument("--daylight", help="daylight", action="store_true")
    parser.add_argument("--CW", help="Cold White", action="store_true")
    parser.add_argument("--nightlight", help="nightlight", action="store_true")
    parser.add_argument("--relax", help="relax", action="store_true")
    parser.add_argument("--TVtime", help="TVtime", action="store_true")
    parser.add_argument("--comfort", help="comfort", action="store_true")
    parser.add_argument("--focused", help="focused", action="store_true")
    parser.add_argument("--fireplace", help="fireplace", action="store_true")
    parser.add_argument("--club", help="club", action="store_true")
    parser.add_argument("--romantic", help="romantic", action="store_true")
    parser.add_argument("--gentle", help="gentle", action="store_true")
    parser.add_argument("--summer", help="summer", action="store_true")
    parser.add_argument("--jungle", help="jungle", action="store_true")
    parser.add_argument("--ocean", help="ocean", action="store_true")
    parser.add_argument("--fall", help="fall", action="store_true")
    parser.add_argument("--sunset", help="sunset", action="store_true")
    parser.add_argument("--party", help="party", action="store_true")
    parser.add_argument("--spring", help="spring", action="store_true")
    parser.add_argument("--forest", help="forest", action="store_true")
    parser.add_argument("--deep_sea", help="deep_sea", action="store_true")
    parser.add_argument("--tropical", help="tropical", action="store_true")
    parser.add_argument("--magic", help="magic Mood", action="store_true")
    parser.add_argument("--mystic", help="Mystic Mountain", action="store_true")
    parser.add_argument("--cotton", help="Cotton Candy", action="store_true")
    parser.add_argument("--ice", help="Ice Cream", action="store_true")

    sub = parser.add_subparsers(title="subcommands", dest='command')

    req = sub.add_parser('get', help='send state request')
    req.add_argument('--all', help='If this flag is set, the whole state will be requested', action='store_true')
    req.add_argument('--power', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--cleaning', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--beeping', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--battery', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--sidebrush', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--rollingbrush', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--filter', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--carpetbooster', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--area', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--time', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--calibrationtime', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--workingmode', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--workingstatus', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--suction', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--water', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--direction', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--errors', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--cleaningrec', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--equipmentmodel', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--alarmmessages', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--commissioninfo', help='If this flag is set, the state element will be requested', action='store_true')
    req.add_argument('--mcu', help='Ask if mcu is online', action='store_true')

    #device specific
    set_parser = sub.add_parser("set", help='enables use of the vc1 control arguments and will control vc1')
    set_parser.add_argument('--power', choices=['on', 'off'], help='turn power on/off')
    set_parser.add_argument('--cleaning', choices=['on', 'off'], help='turn cleaning on/off')
    set_parser.add_argument('--beeping', choices=['on', 'off'], help='enable/disable the find-vc function')
    set_parser.add_argument('--carpetbooster', metavar='strength', type=int, help='set the carpet booster strength (0-255)')
    set_parser.add_argument('--workingmode', choices=[m.name for m in VC_WORKINGMODE], help='set the working mode')
    set_parser.add_argument('--water', choices=['LOW', 'MID', 'HIGH'], help='set water quantity')
    set_parser.add_argument('--suction', choices=[m.name for m in VC_SUCTION_STRENGTHS], help='set suction power')
    set_parser.add_argument('--direction', choices=['FORWARDS','BACKWARDS', 'TURN_LEFT', 'TURN_RIGHT', 'STOP'], help='manually control movement')
    set_parser.add_argument('--commissioninfo', type=str, help='set up to 256 characters of commisioning info')
    set_parser.add_argument('--calibrationtime', metavar='time', type=int, help='set the calibration time (1-1999999999)')

    reset_parser = sub.add_parser("reset", help='enables resetting consumables')
    reset_parser.add_argument('--sidebrush', help='resets the sidebrush life counter', action='store_true')
    reset_parser.add_argument('--rollingbrush', help='resets the rollingbrush life counter', action='store_true')
    reset_parser.add_argument('--filter', help='resets the filter life counter', action='store_true')


PROD_HOST = "https://app-api.prod.qconnex.io"
TEST_HOST = "https://app-api.test.qconnex.io"


SEND_LOOP_MAX_SLEEP_TIME = 0.05
MSG_COUNTER = 0


class Data_communicator:
    def __init__(self, server_ip: str = "0.0.0.0") -> None:
        self.tcp: socket.socket = None
        self.udp: socket.socket = None
        self.server_ip: str = server_ip

    def shutdown(self) -> None:

        try:
            if self.tcp:
                self.tcp.shutdown(socket.SHUT_RDWR)
                self.tcp.close()
                LOGGER.debug("Closed TCP port 3333")
                self.tcp = None
        except:
            pass

        try:
            if self.udp:
                self.udp.close()
                LOGGER.debug("Closed UDP port 2222")
                self.udp = None
        except:
            pass

    async def bind_ports(self) -> bool:
        """bind ports."""
        # await tcp_udp_port_lock.acquire()
        self.shutdown()
        server_address: tuple[str, int]
        try:

            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if self.server_ip is not None:
                server_address = (self.server_ip, 2222)
            else:
                server_address = ("0.0.0.0", 2222)
            self.udp.bind(server_address)
            LOGGER.debug("Bound UDP port 2222")

        except Exception as e:
            LOGGER.error(
                "Error on opening and binding the udp port 2222 on host for initiating the device communication."
            )
            return False

        try:
            self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_address = ("0.0.0.0", 3333)
            self.tcp.bind(server_address)
            LOGGER.debug("Bound TCP port 3333")
            self.tcp.listen(1)

        except Exception as e:
            LOGGER.error(
                "Error on opening and binding the tcp port 3333 on host for initiating the device communication."
            )
            return False
        return True


class Klyqa_account:
    """

    Klyqa account
    * rest access token
    * devices
    * account settings

    """

    host: str = ""
    access_token: str = ""
    username: str
    password: str
    username_cached: bool

    devices: dict[str, KlyqaDevice] = {}

    acc_settings = {}
    acc_settings_cached: bool

    __acc_settings_lock: asyncio.Lock
    _settings_loaded_ts: datetime.datetime

    __send_loop_sleep: asyncio.Task
    __tasks_done: asyncio.Task
    __tasks_undone: asyncio.Task
    __read_tcp_task: asyncio.Task
    message_queue: dict[tuple] = {}
    message_queue_new: list[tuple] = []
    search_and_send_loop_task: asyncio.Task
    tcp: socket
    udp: socket

    def __init__(
        self, data_communicator: Data_communicator, username="", password="", host=""
    ):
        """Initialize the account with the login data, tcp, udp datacommunicator and tcp
        communication tasks."""
        self.username = username
        self.password = password
        self.access_token: str = ""
        self.host = PROD_HOST if not host else host
        self.username_cached = False
        self.acc_settings_cached = False
        self.__acc_settings_lock = asyncio.Lock()
        self._settings_loaded_ts = None
        self.__send_loop_sleep = None
        self.__tasks_done = []
        self.__tasks_undone = []
        self.message_queue: dict[tuple] = {}
        self.message_queue_new: list[tuple] = []
        self.search_and_send_loop_task: asyncio.Task = None
        self.__read_tcp_task: asyncio.Task = None
        self.tcp = data_communicator.tcp if data_communicator else None
        self.udp = data_communicator.udp if data_communicator else None
        self.data_communicator: Data_communicator = data_communicator
        self.search_and_send_loop_task_end_now = False

    async def device_handle_local_tcp(self, device: KlyqaDevice):
        """Handle the incoming tcp connection to the device."""
        return_state = -1
        response = ""

        try:
            LOGGER.debug(f"TCP layer connected {device.local.address['ip']}")

            r_device: RefParse = RefParse(device)
            msg_sent: Message = None
            r_msg: RefParse = RefParse(msg_sent)

            LOGGER.debug(f"started tcp device {device.local.address['ip']}")
            try:
                return_state = await self.aes_handshake_and_send_msgs(r_device, r_msg)
                device = r_device.ref
                msg_sent = r_msg.ref
            except CancelledError as e:
                LOGGER.error(
                    f"Cancelled local send because send-timeout send_timeout hitted {device.local.address['ip']}, "
                    + (device.u_id if device.u_id else "")
                    + "."
                )
            except Exception as e:
                LOGGER.debug(f"{traceback.format_exc()}")
            finally:
                LOGGER.debug(
                    f"finished tcp device {device.local.address['ip']}, return_state: {return_state}"
                )

                if msg_sent and not msg_sent.callback is None:
                    await msg_sent.callback(msg_sent, device.u_id)
                    LOGGER.debug(f"device {device.u_id} answered msg {msg_sent.msg_queue}")

                # if not device or (device and not device.u_id in self.message_queue or not self.message_queue[device.u_id]):
                #     try:
                # LOGGER.debug(f"no more messages to sent for device {device.u_id}, close tcp tunnel.")
                device.local.connection.shutdown(socket.SHUT_RDWR)
                device.local.connection.close()
                device.local.connection = None
                LOGGER.debug(f"tcp closed for device.u_id.")
                # except Exception as e:
                #     pass

                unit_id: str = f" Unit-ID: {device.u_id}" if device.u_id else ""

                if return_state == 0:
                    """no error"""

                    def dict_values_to_list(d: dict) -> str:
                        r = []
                        for i in d.values():
                            if isinstance(i, dict):
                                i = dict_values_to_list(i)
                            r.append(str(i))
                        return r

                    # if not args.selectDevice:
                    #     name = f' "{device.get_name()}"' if device.get_name() else ""
                    #     LOGGER.info(
                    #         f"device{name} response (local network): "
                    #         + str(json.dumps(response, sort_keys=True, indent=4))
                    #     )

                if device.u_id and device.u_id in self.devices:
                    device_b: KlyqaDevice = self.devices[device.u_id]
                    if device_b._use_thread == asyncio.current_task():
                        try:
                            device_b._use_lock.release()
                            device_b._use_thread = None
                        except:
                            pass

                elif return_state == 1:
                    LOGGER.error(
                        f"Unknown error during send (and handshake) with device {unit_id}."
                    )
                elif return_state == 2:
                    pass
                    # LOGGER.debug(f"Wrong device unit id.{unit_id}")
                elif return_state == 3:
                    LOGGER.debug(
                        f"End of tcp stream. ({device.local.address['ip']}:{device.local.address['port']})"
                    )

        except CancelledError as e:
            LOGGER.error(f"Device tcp task cancelled.")
        except Exception as e:
            LOGGER.debug(f"{e}")
            pass
        return return_state
        pass

    async def search_and_send_to_device(self, timeout_ms=DEFAULT_SEND_TIMEOUT_MS) -> bool:
        """Send broadcast and make tasks for incoming tcp connections."""
        loop = asyncio.get_event_loop()

        try:
            if (
                not self.data_communicator.tcp or not self.data_communicator.udp
            ):
                await self.data_communicator.bind_ports()
            while not self.search_and_send_loop_task_end_now:  # self.tcp:
                if (
                    not self.data_communicator.tcp or not self.data_communicator.udp
                ):
                    break
                # for debug cursor jump:
                a = False
                if a:
                    break

                # while self.message_queue_new:
                #     """add start timestamp to new messages"""
                #     send_msg, target_device_uid, args, callback, time_to_live_secs, started = self.message_queue_new.pop(0)
                #     if not send_msg:
                #         LOGGER.error(f"No message queue to send in message to {target_device_uid}!")
                #         await callback(None, target_device_uid)
                #         continue

                #     msg = Message(datetime.datetime.now(), send_msg, args,
                #     target_uid = target_device_uid, callback = callback, time_to_live_secs = time_to_live_secs)

                #     if not await msg.check_msg_ttl():
                #         continue

                #     LOGGER.debug(f"new message {msg.msg_counter} target {target_device_uid} {send_msg}")

                #     self.message_queue.setdefault(target_device_uid, []).append(msg)

                if self.message_queue:

                    read_broadcast_response = True
                    try:
                        LOGGER.debug("Broadcasting QCX-SYN Burst")
                        self.data_communicator.udp.sendto(
                            "QCX-SYN".encode("utf-8"), ("255.255.255.255", 2222)
                        )

                    except Exception as exception:
                        LOGGER.debug("Broadcasting QCX-SYN Burst Exception")
                        LOGGER.debug(f"{traceback.format_exc()}")
                        read_broadcast_response = False
                        if not await self.data_communicator.bind_ports():
                            LOGGER.error("Error binding ports udp 2222 and tcp 3333.")
                            return False

                    if not read_broadcast_response:
                        try:
                            LOGGER.debug(f"sleep task create (broadcasts)..")
                            self.__send_loop_sleep = loop.create_task(
                                asyncio.sleep(
                                    SEND_LOOP_MAX_SLEEP_TIME
                                    if (
                                        len(self.message_queue) > 0
                                        or len(self.message_queue_new) > 0
                                    )
                                    else 1000000000
                                )
                            )

                            LOGGER.debug(f"sleep task wait..")
                            done, pending = await asyncio.wait([self.__send_loop_sleep])

                            LOGGER.debug(f"sleep task done..")
                        except CancelledError as e:
                            LOGGER.debug(f"sleep cancelled1.")
                        except Exception as e:
                            LOGGER.debug(f"{e}")
                            pass
                        pass

                    while read_broadcast_response:

                        timeout_read: float = 1.9
                        LOGGER.debug("Read again tcp port..")

                        async def read_tcp_task():
                            try:
                                return await loop.run_in_executor(
                                    None,
                                    select.select,
                                    [self.data_communicator.tcp],
                                    [],
                                    [],
                                    timeout_read,
                                )
                            except CancelledError as e:
                                LOGGER.debug("cancelled tcp reading.")
                            except Exception as e:
                                LOGGER.error(f"{traceback.format_exc()}")
                                if not await self.data_communicator.bind_ports():
                                    LOGGER.error(
                                        "Error binding ports udp 2222 and tcp 3333."
                                    )

                        self.__read_tcp_task = asyncio.create_task(read_tcp_task())

                        LOGGER.debug("Started tcp reading..")
                        try:
                            await asyncio.wait_for(self.__read_tcp_task, timeout=1.0)
                        except Exception as e:
                            LOGGER.debug(
                                f"Socket-Timeout for incoming tcp connections."
                            )

                            if not await self.data_communicator.bind_ports():
                                LOGGER.error(
                                    "Error binding ports udp 2222 and tcp 3333."
                                )

                        result = self.__read_tcp_task.result()
                        if (
                            not result
                            or not isinstance(result, tuple)
                            or not len(result) == 3
                        ):  # or self.__read_tcp_task.cancelled():
                            LOGGER.debug("no tcp read result. break")
                            break
                        readable, _, _ = self.__read_tcp_task.result()
                        # readable, _, _ = await loop.run_in_executor(
                        #     None, select.select, [self.data_communicator.tcp], [], [], timeout_read)
                        LOGGER.debug("Reading tcp port done..")

                        if not self.data_communicator.tcp in readable:
                            break
                        else:
                            device = KlyqaDevice()
                            device.local.connection, addr = self.data_communicator.tcp.accept()
                            device.local.address["ip"] = addr[0]
                            device.local.address["port"] = addr[1]

                            new_task = loop.create_task(
                                self.device_handle_local_tcp(device)
                            )

                            # for test:
                            await asyncio.wait([new_task], timeout=0.00000001)
                            # timeout task for the device tcp task
                            loop.create_task(
                                asyncio.wait_for(new_task, timeout=(timeout_ms / 1000))
                            )

                            LOGGER.debug(
                                f"Address {device.local.address['ip']} process task created."
                            )
                            self.__tasks_undone.append(
                                (new_task, datetime.datetime.now())
                            )  # device.u_id

                    try:
                        to_del = []
                        """check message queue for ttls"""
                        for uid, msgs in self.message_queue.items():
                            for msg in msgs:
                                if not await msg.check_msg_ttl():
                                    msgs.remove(msg)
                                if not self.message_queue[uid]:
                                    # del self.message_queue[uid]
                                    to_del.append(uid)
                                    break
                        for uid in to_del:
                            del self.message_queue[uid]
                    except Exception as e:
                        LOGGER.debug(f"{traceback.format_exc()}")
                        pass

                try:
                    tasks_undone_new = []
                    for task, started in self.__tasks_undone:
                        if task.done():
                            self.__tasks_done.append(
                                (task, started, datetime.datetime.now())
                            )
                            e = task.exception()
                            if e:
                                LOGGER.debug(f"Exception error in {task._coro}: {e}")
                        else:
                            if datetime.datetime.now() - started > datetime.timedelta(
                                milliseconds=int(timeout_ms * 1000)
                            ):
                                task.cancel()
                            tasks_undone_new.append((task, started))
                    self.__tasks_undone = tasks_undone_new

                except CancelledError as e:
                    LOGGER.debug(f"__tasks_undone check cancelled.")
                except Exception as e:
                    LOGGER.debug(f"{e}")
                    pass
                pass

                if not len(self.message_queue_new) and not len(self.message_queue):
                    try:
                        LOGGER.debug(f"sleep task create2 (searchandsendloop)..")
                        self.__send_loop_sleep = loop.create_task(
                            asyncio.sleep(
                                SEND_LOOP_MAX_SLEEP_TIME
                                if len(self.message_queue) > 0
                                else 1000000000
                            )
                        )
                        LOGGER.debug(f"sleep task wait..")
                        done, pending = await asyncio.wait([self.__send_loop_sleep])
                        LOGGER.debug(f"sleep task done..")
                    except CancelledError as e:
                        LOGGER.debug(f"sleep cancelled2.")
                    except Exception as e:
                        LOGGER.debug(f"{e}")
                        pass
                pass

        except CancelledError as e:
            LOGGER.debug(f"search and send to device loop cancelled.")
            self.message_queue = {}
            self.message_queue_now = {}
            for task, started in self.__tasks_undone:
                task.cancel()
        except Exception as e:
            LOGGER.debug("Exception on send and search loop. Stop loop.")
            LOGGER.debug(f"{traceback.format_exc()}")
            return False
        return True

    async def search_and_send_loop_task_stop(self):
        while (
            self.search_and_send_loop_task and not self.search_and_send_loop_task.done()
        ):
            LOGGER.debug("stop send and search loop.")
            if self.search_and_send_loop_task:
                self.search_and_send_loop_task_end_now = True
                self.search_and_send_loop_task.cancel()
            try:
                LOGGER.debug("wait for send and search loop to end.")
                await asyncio.wait_for(self.search_and_send_loop_task, timeout=0.1)
                LOGGER.debug("wait end for send and search loop.")
            except Exception as e:
                LOGGER.debug(f"{traceback.format_exc()}")
            LOGGER.debug("wait end for send and search loop.")
        pass

    def search_and_send_loop_task_alive(self) -> None:

        loop = asyncio.get_event_loop()

        if not self.search_and_send_loop_task or self.search_and_send_loop_task.done():
            LOGGER.debug("search and send loop task created.")
            self.search_and_send_loop_task = asyncio.create_task(
                self.search_and_send_to_device()
            )
        try:
            self.__send_loop_sleep.cancel()
        except:
            pass

    async def set_send_message(
        self,
        send_msg,
        target_device_uid,
        args,
        callback=None,
        time_to_live_secs=-1.0,
        started=datetime.datetime.now(),
    ) -> bool:

        loop = asyncio.get_event_loop()
        # self.message_queue_new.append((send_msg, target_device_uid, args, callback, time_to_live_secs, started))

        if not send_msg:
            LOGGER.error(f"No message queue to send in message to {target_device_uid}!")
            await callback(None, target_device_uid)
            return False

        msg: Message = Message(
            datetime.datetime.now(),
            send_msg,
            args,
            target_uid=target_device_uid,
            callback=callback,
            time_to_live_secs=time_to_live_secs,
        )

        if not await msg.check_msg_ttl():
            return False

        LOGGER.debug(
            f"new message {msg.msg_counter} target {target_device_uid} {send_msg}"
        )

        self.message_queue.setdefault(target_device_uid, []).append(msg)

        if self.__read_tcp_task:
            self.__read_tcp_task.cancel()
        self.search_and_send_loop_task_alive()
        return True

    async def load_username_cache(self) -> None:
        acc_settings_cache, cached = await async_json_cache(
            None, "last.acc_settings.cache.json"
        )

        self.username_cached = cached

        if cached:
            LOGGER.info(f"No username or no password given using cache.")
            if not acc_settings_cache or (
                self.username and list(acc_settings_cache.keys())[0] != self.username
            ):
                e = f"Account settings are from another account than {self.username}."
                LOGGER.error(e)
                raise ValueError(e)
            else:
                try:
                    self.username = [list(acc_settings_cache.keys())[0]]
                    self.password = [acc_settings_cache[self.username]["password"]]
                    e = f"Using cache account settings from account {self.username}."
                    LOGGER.info(e)
                except:
                    e = f"Could not load cached account settings."
                    LOGGER.error(e)
                    raise ValueError(e)
        else:
            e = f"Could not load cached account settings."
            LOGGER.error(e)
            raise ValueError(e)

    async def login(self, print_onboarded_devices=False) -> bool:
        """Login on klyqa account, get account settings, get onboarded device profiles,
        print all devices if parameter set."""
        global device_configs
        loop = asyncio.get_event_loop()

        acc_settings_cache = {}
        if not self.username or not self.password:
            try:
                async with aiofiles.open(
                    os.path.dirname(sys.argv[0]) + f"/last_username", mode="r"
                ) as f:
                    self.username = await f.readline(self.username).strip()
            except:
                return False

        if self.username is not None and self.password is not None:
            login_response = None
            try:
                login_data = {"email": self.username, "password": self.password}

                login_response: requests.Response = await loop.run_in_executor(
                    None,
                    functools.partial(
                        requests.post,
                        self.host + "/auth/login",
                        json=login_data,
                        timeout=10,
                    ),
                )

                if not login_response or (
                    login_response.status_code != 200
                    and login_response.status_code != 201
                ):
                    LOGGER.error(
                        str(login_response.status_code)
                        + ", "
                        + str(login_response.text)
                    )
                    raise Exception(login_response.text)
                login_json = json.loads(login_response.text)
                self.access_token = login_json.get("accessToken")
                # self.acc_settings = await loop.run_in_executor(
                #     None, functools.partial(self.request, "settings", timeout=30)
                # )
                self.acc_settings = await self.request("settings", timeout=30)

            except Exception as e:
                LOGGER.error(
                    f"Error during login. Try reading account settings for account {self.username} from cache."
                )
                try:
                    acc_settings_cache, cached = await async_json_cache(
                        None, f"{self.username}.acc_settings.cache.json"
                    )
                except:
                    return False
                if not cached:
                    return False
                else:
                    self.acc_settings = acc_settings_cache

            if not self.acc_settings:
                return False

            try:
                acc_settings_cache = {
                    **self.acc_settings,
                    **{
                        "time_cached": datetime.datetime.now(),
                        "password": self.password,
                    },
                }

                """save current account settings in cache"""
                await async_json_cache(
                    acc_settings_cache, f"{self.username}.acc_settings.cache.json"
                )

                async with aiofiles.open(
                    os.path.dirname(sys.argv[0]) + f"/last_username", mode="w"
                ) as f:
                    await f.write(self.username)

            except Exception as e:
                pass

            try:
                klyqa_acc_string = (
                    "Klyqa account " + self.username + ". Onboarded devices:"
                )
                sep_width = len(klyqa_acc_string)

                if print_onboarded_devices:
                    print(sep_width * "-")
                    print(klyqa_acc_string)
                    print(sep_width * "-")

                queue_printer: EventQueuePrinter = EventQueuePrinter()

                def device_request_and_print(device_sets):
                    state_str = (
                        f'Name: "{device_sets["name"]}"'
                        + f'\tAES-KEY: {device_sets["aesKey"]}'
                        + f'\tUnit-ID: {device_sets["localDeviceId"]}'
                        + f'\tCloud-ID: {device_sets["cloudDeviceId"]}'
                        + f'\tType: {device_sets["productId"]}'
                    )
                    cloud_state = None

                    device: KlyqaDevice
                    if device_sets["productId"].find(".lighting") > -1:
                        device = KlyqaBulb()
                    elif device_sets["productId"].find(".cleaning") > -1:
                        device = KlyqaVC()
                    else:
                        return
                    device.u_id = format_uid(device_sets["localDeviceId"])
                    device.acc_sets = device_sets

                    self.devices[format_uid(device_sets["localDeviceId"])] = device

                    async def req():
                        try:
                            ret = await self.request(
                                f'device/{device_sets["cloudDeviceId"]}/state', timeout=30
                            )
                            return ret
                        except Exception as e:
                            return None

                    try:
                        cloud_state = asyncio.run(req())
                        if cloud_state:
                            if "connected" in cloud_state:
                                state_str = (
                                    state_str
                                    + f'\tCloud-Connected: {cloud_state["connected"]}'
                                )
                            device.cloud.connected = cloud_state["connected"]

                            device.save_device_message(
                                {**cloud_state, **{"type": "status"}}
                            )
                        else:
                            raise
                    except:
                        err = f'No answer for cloud device state request {device_sets["localDeviceId"]}'
                        # if args.cloud:
                        #     LOGGER.error(err)
                        # else:
                        LOGGER.info(err)

                    if print_onboarded_devices:
                        queue_printer.print(state_str)

                device_state_req_threads = []

                product_ids: set[str] = set()
                if self.acc_settings and "devices" in self.acc_settings:
                    for device_sets in self.acc_settings["devices"]:
                        # if not device_sets["productId"].startswith("@klyqa.lighting"):
                        #     continue
                        device_state_req_threads.append(
                            Thread(target=device_request_and_print, args=(device_sets,))
                        )
                        t = Thread(target=device_request_and_print, args=(device_sets,))
                        t.start()
                        t.join()

                        if isinstance(AES_KEYs, dict):
                            AES_KEYs[
                                format_uid(device_sets["localDeviceId"])
                            ] = bytes.fromhex(device_sets["aesKey"])
                        product_ids.add(device_sets["productId"])

                # for t in device_state_req_threads:
                #     t.start()
                # for t in device_state_req_threads:
                #     t.join()

                queue_printer.stop()

                def get_conf(id, device_configs):
                    async def req():
                        try:
                            ret = await self.request("config/product/" + id, timeout=30)
                            return ret
                        except:
                            return None

                    config = asyncio.run(req())
                    if config:
                        device_config: Device_config = config
                        device_configs[id] = device_config

                if self.acc_settings and product_ids:
                    threads = [
                        Thread(target=get_conf, args=(i, device_configs))
                        for i in product_ids
                    ]
                    for t in threads:
                        LOGGER.debug(
                            "Try to request device config for "
                            + t._args[0]
                            + " from server."
                        )
                        t.start()
                    for t in threads:
                        t.join()

                device_configs, cached = await async_json_cache(
                    device_configs, "device.configs.json"
                )
                if cached:
                    LOGGER.info("No server reply for device configs. Using cache.")

            except Exception as e:
                LOGGER.error("Error during login to klyqa: " + str(e))
                return False
        return True

    def get_header_default(self) -> dict[str, str]:
        header: dict[str, str] = {
            "X-Request-Id": str(uuid.uuid4()),
            "Accept": "application/json",
            "Content-Type": "application/json",
            "accept-encoding": "gzip, deflate, utf-8",
        }
        return header

    def get_header(self) -> dict[str, str]:
        return {
            **self.get_header_default(),
            **{"Authorization": "Bearer " + self.access_token},
        }

    async def request(self, url, **kwargs):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            functools.partial(
                requests.get,
                self.host + "/" + url,
                headers=self.get_header()
                if self.access_token
                else self.get_header_default(),
                **kwargs,
            ),
        )
        if response.status_code != 200:
            # TODO: make here a right
            raise Exception(response.text)
        return json.loads(response.text)

    async def post(self, url, **kwargs):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            functools.partial(
                requests.post,
                self.host + "/" + url,
                headers=self.get_header(),
                **kwargs,
            ),
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return json.loads(response.text)

    def shutdown(self):
        """Logout again from klyqa account."""
        for uid in self.devices:
            try:
                device = self.devices[uid]
                device.local.connection.shutdown(socket.SHUT_RDWR)
                device.local.connection.close()
                device.local.connection = None
            except Exception as excp:
                pass
        if self.access_token:
            try:
                response = requests.post(
                    self.host + "/auth/logout", headers=self.get_header_default()
                )
                self.access_token = ""
            except Exception as excp:
                LOGGER.warning("Couldn't logout.")

    async def aes_handshake_and_send_msgs(
        self,
        r_device: RefParse,
        r_msg: RefParse,
        use_dev_aes=False,
        timeout_ms=11000, # currently only used for pause timeout between sending messages if multiple for device in queue to send.
    ) -> ReturnTuple:
        """

        Finish AES handshake.
        Getting the identity of the device.
        Send the commands in message queue to the device with the device u_id or to any device.

        params:
            device: Device - (initial) device object with the tcp connection
            target_device_uid - If given device_uid only send commands when the device unit id equals the target_device_uid
            discover_mode - if True do the process to any device unit id.

        returns: tuple[int, dict] or tuple[int, str]
                dict: Json response of the device
                str: Error string message
                int: Error type
                    0 - success - no error
                    1 - on error
                    2 - not correct device uid
                    3 - tcp connection ended, shall retry
                    4 - error on reading response message from device, shall retry
                    5 - error getting lock for device, shall retry
                    6 - missing aes key
                    7 - value not valid for device config

        """

        global sep_width, LOGGER
        device: KlyqaDevice = r_device.ref

        data = []
        last_send: datetime.datetime = datetime.datetime.now()
        device.local.connection.settimeout(0.001)
        pause: datetime.timedelta = datetime.timedelta(milliseconds=0)
        elapsed: datetime.timedelta = datetime.datetime.now() - last_send

        loop = asyncio.get_event_loop()

        return_val = Device_TCP_return.nothing_done

        msg_sent: Message = None
        communication_finished: bool = False

        async def __send_msg(msg):
            nonlocal last_send, pause, return_val, device

            LOGGER.debug(f"Sent msg '{msg.msg_queue}' to device '{device.u_id}'.")

            def rm_msg() -> None:
                try:
                    LOGGER.debug(f"rm_msg()")
                    self.message_queue[device.u_id].remove(msg)
                    msg.state = Message_state.sent

                    if (
                        device.u_id in self.message_queue
                        and not self.message_queue[device.u_id]
                    ):
                        del self.message_queue[device.u_id]
                except Exception as e:
                    LOGGER.debug(traceback.format_exc())

            return_val = Device_TCP_return.sent

            if len(msg.msg_queue) and len(msg.msg_queue[-1]) == 2:
                text, ts = msg.msg_queue.pop()
                msg.msg_queue_sent.append(text)
            else:
                text, ts, check_func = msg.msg_queue.pop()
                msg.msg_queue_sent.append(text)
                if not check_func(product_id=device.ident.product_id):
                    rm_msg()
                    # return (7, "value not valid for device config")
                    return None

            pause = datetime.timedelta(milliseconds=timeout_ms)
            try:
                if await loop.run_in_executor(None, send_msg, text, device):
                    rm_msg()
                    last_send = datetime.datetime.now()
                    return msg
            except Exception as excep:
                LOGGER.debug(traceback.format_exc())
                # return (1, "error during send")
            return None

        while not communication_finished and (
            len(self.message_queue) > 0 or elapsed < pause
        ):
            try:
                data = await loop.run_in_executor(
                    None, device.local.connection.recv, 4096
                )
                if len(data) == 0:
                    LOGGER.debug("EOF")
                    # return (3, "TCP connection ended.")
                    return Device_TCP_return.tcp_error
            except socket.timeout:
                pass
            except Exception as excep:
                LOGGER.debug(traceback.format_exc())
                # return (1, "unknown error")
                return Device_TCP_return.unknown_error

            elapsed = datetime.datetime.now() - last_send

            if device.local.state == "CONNECTED":
                ## check how the answer come in and how they can be connected to the messages that has been sent.
                i = 0
                try:
                    send_next: bool = elapsed >= pause
                    # if len(message_queue_tx) > 0 and :
                    while (
                        send_next
                        and device.u_id in self.message_queue
                        and i < len(self.message_queue[device.u_id])
                    ):
                        msg = self.message_queue[device.u_id][i]
                        i: int = i + 1
                        if msg.state == Message_state.unsent:
                            msg_sent = await __send_msg(msg)
                            r_msg.ref = msg_sent
                            if not msg_sent:
                                return Device_TCP_return.sent_error
                            else:
                                break
                            # await recv(msg)
                except:
                    pass

            while not communication_finished and (len(data)):
                LOGGER.debug(
                    "TCP server received "
                    + str(len(data))
                    + " bytes from "
                    + str(device.local.address)
                )

                # Read out the data package as follows: package length (pkgLen), package type (pkgType) and package data (pkg)

                pkgLen: int = data[0] * 256 + data[1]
                pkgType: int = data[3]

                pkg: bytes = data[4 : 4 + pkgLen]
                if len(pkg) < pkgLen:
                    LOGGER.debug("Incomplete packet, waiting for more...")
                    break

                data: bytes = data[4 + pkgLen :]

                if device.local.state == "WAIT_IV" and pkgType == 0:

                    # Check identification package from device, lock the device object for changes,
                    # safe the idenfication to device object if it is a not known device,
                    # send the local initial vector for the encrypted communication to the device.

                    LOGGER.debug("Plain: " + str(pkg))
                    json_response: dict[str, Any] = json.loads(pkg)
                    ident: KlyqaDeviceResponseIdent = KlyqaDeviceResponseIdent(**json_response["ident"])
                    device.u_id = ident.unit_id
                    is_new_device = False
                    if device.u_id != "no_uid" and device.u_id not in self.devices:
                        is_new_device = True
                        if self.acc_settings:
                            dev: list[KlyqaDevice] = [
                                device2
                                for device2 in self.acc_settings["devices"]
                                if format_uid(device2["localDeviceId"])
                                == format_uid(device.u_id)
                            ]
                            if dev:
                                device.acc_sets = dev[0]
                        if ident.product_id.startswith(
                            "@klyqa.lighting"
                        ):
                            self.devices[device.u_id] = KlyqaBulb()
                        if ident.product_id.startswith(
                            "@klyqa.cleaning"
                        ):
                            self.devices[device.u_id] = KlyqaVC()

                    # device_b: KlyqaDevice
                    # device.ident.product_id.startswith("@klyqa.cleaning"):
                    #     device_b: KlyqaDevice = self.devices[device.u_id]

                    # cached client device (self.devices), incoming device object created on tcp connection acception
                    device_b: KlyqaDevice = self.devices[device.u_id]
                    if await device_b.use_lock():

                        if not is_new_device:
                            try:
                                """There shouldn't be an open connection on the already known cached devices, but if there accidently is close it."""
                                device_b.local.connection.shutdown(socket.SHUT_RDWR)
                                device_b.local.connection.close()
                                LOGGER.debug(f"tcp closed for device.u_id.")
                                """just ensure connection is closed, so that device knows it as well"""
                            except:
                                pass

                        device_b.local = device.local
                        device = device_b
                        r_device.ref = device_b
                    else:
                        err: str = f"Couldn't get use lock for device {device_b.get_name()} {device.local.address})"
                        LOGGER.error(err)
                        return Device_TCP_return.device_lock_timeout

                    device.local.received_packages.append(json_response)
                    device.save_device_message(json_response)

                    if (
                        not device.u_id in self.message_queue
                        or not self.message_queue[device.u_id]
                    ):
                        if device.u_id in self.message_queue:
                            del self.message_queue[device.u_id]
                        return Device_TCP_return.no_message_to_send

                    found = ""
                    settings_device = ""
                    if self.acc_settings and "devices" in self.acc_settings:
                        settings_device = [
                            device_sets
                            for device_sets in self.acc_settings["devices"]
                            if format_uid(device_sets["localDeviceId"])
                            == format_uid(device.u_id)
                        ]
                    if settings_device:
                        name = settings_device[0]["name"]
                        found = found + ' "' + name + '"'
                    else:
                        found = found + f" {json_response['ident']['unit_id']}"

                    LOGGER.info("Found device" + found)
                    AES_KEY = ""
                    if "all" in AES_KEYs:
                        AES_KEY = AES_KEYs["all"]
                    elif use_dev_aes or "dev" in AES_KEYs:
                        AES_KEY = AES_KEY_DEV
                    elif isinstance(AES_KEYs, dict) and device.u_id in AES_KEYs:
                        AES_KEY = AES_KEYs[device.u_id]
                    try:
                        device.local.connection.send(
                            bytes([0, 8, 0, 1]) + device.local.localIv
                        )
                    except:
                        # return (1, "Couldn't send local IV.")
                        return Device_TCP_return.err_local_iv

                if device.local.state == "WAIT_IV" and pkgType == 1:

                    # Receive the remote initial vector (iv) for aes encrypted communication.

                    device.local.remoteIv = pkg
                    device.local.received_packages.append(pkg)
                    if not AES_KEY:
                        LOGGER.error(
                            "Missing AES key. Probably not in onboarded devices. Provide AES key with --aes [key]! "
                            + str(device.u_id)
                        )
                        # return (6, "missing aes key")
                        return Device_TCP_return.missing_aes_key
                    device.local.sendingAES = AES.new(
                        AES_KEY, AES.MODE_CBC, iv=device.local.localIv + device.local.remoteIv
                    )
                    device.local.receivingAES = AES.new(
                        AES_KEY, AES.MODE_CBC, iv=device.local.remoteIv + device.local.localIv
                    )

                    device.local.state = "CONNECTED"

                elif device.local.state == "CONNECTED" and pkgType == 2:

                    # Receive encrypted answer for sent message.

                    cipher: bytes = pkg

                    plain: bytes = device.local.receivingAES.decrypt(cipher)
                    device.local.received_packages.append(plain)
                    msg_sent.answer = plain
                    json_response = ""
                    try:
                        plain_utf8: str = plain.decode()
                        json_response = json.loads(plain_utf8)
                        device.save_device_message(json_response)
                        device.local.sent_msg_answer = json_response
                        device.local.aes_key_confirmed = True
                        LOGGER.debug(
                            f"buld uid {device.u_id} aes_confirmed {device.local.aes_key_confirmed}"
                        )
                    except:
                        LOGGER.error("Could not load json message from device: ")
                        LOGGER.error(str(pkg))
                        # return (4, "Could not load json message from device.")
                        return Device_TCP_return.response_error

                    msg_sent.answer_utf8 = plain_utf8
                    msg_sent.answer_json = json_response
                    msg_sent.state = Message_state.answered
                    return_val = Device_TCP_return.answered

                    device.recv_msg_unproc.append(msg_sent)
                    device.process_msgs()

                    LOGGER.debug("Request's reply decrypted: " + str(plain))
                    # return (0, json_response)
                    communication_finished = True
                    break
                    return return_val
        return return_val

    async def request_account_settings_eco(self) -> bool:
        if not await self.__acc_settings_lock.acquire():
            return False
        try:
            ret = False
            now = datetime.datetime.now()
            if not self._settings_loaded_ts or (
                now - self._settings_loaded_ts
                >= datetime.timedelta(seconds=self.scan_interval)
            ):
                """look that the settings are loaded only once in the scan interval"""
                ret = await self.request_account_settings()
        finally:
            self.__acc_settings_lock.release()
        return ret

    async def request_account_settings(self) -> None:
        try:
            self.acc_settings: TypeJSON = await self.request("settings")

            """saving updated account settings to cache"""

            # acc_settings_cache = (
            #     {args.username[0]: self.acc_settings} if self.acc_settings else {}
            # )

            # self.acc_settings, cached = await async_json_cache(
            #     acc_settings_cache, "last.acc_settings.cache.json"
            # )

            # if cached:
            #     LOGGER.info(
            #         f"No server reply for account settings {args.username[0]}. Using cache."
            #     )
            #     if (
            #         not self.acc_settings
            #         or list(self.acc_settings.keys())[0] != args.username[0]
            #     ):
            #         LOGGER.error(
            #             f"Account settings are from another account than "
            #             + f"{args.username[0]}."
            #         )
            #         return False
        except:
            pass

        # self.acc_settings = self.acc_settings[list(self.acc_settings.keys())[0]]

    async def _send_to_devices(
        self,
        args,
        args_in,
        udp: socket = None,
        tcp: socket = None,
        timeout_ms=5000,
        async_answer_callback: Callable[[Message, str], Any] = None,
    ):
        """Collect the messages for the devices to send to

        Args:
            args (Argsparse): Parsed args object
            args_in (list): List of arguments parsed to the script call
            timeout_ms (int, optional): Timeout to send. Defaults to 5000.

        Raises:
            Exception: Network or file errors

        Returns:
            bool: True if succeeded.
        """
        if not udp:
            udp = self.data_communicator.udp
        if not tcp:
            tcp = self.data_communicator.tcp
        try:
            global sep_width, device_configs

            loop = asyncio.get_event_loop()

            send_started: datetime.datetime = datetime.datetime.now()

            if args.dev:
                args.local = True
                args.tryLocalThanCloud = False
                args.cloud = False

            if args.debug:
                LOGGER.setLevel(level=logging.DEBUG)
                logging_hdl.setLevel(level=logging.DEBUG)

            if args.cloud or args.local:
                args.tryLocalThanCloud = False

            target_device_uids = set()

            message_queue_tx_local = []
            message_queue_tx_state_cloud = []
            message_queue_tx_command_cloud = []

            # TODO: Missing cloud discovery and interactive device selection. Send to devices if given as argument working.
            if (args.local or args.tryLocalThanCloud) and (
                not args.device_name
                and not args.device_unitids
                and not args.allDevices
                and not args.discover
            ):
                discover_local_args: list[str] = [
                    "--request",
                    "--allDevices",
                    "--selectDevice",
                    "--discover"
                ]

                orginal_args_parser: ArgumentParser = get_description_parser()
                discover_local_args_parser: ArgumentParser = get_description_parser()

                add_config_args(parser=orginal_args_parser)
                add_config_args(parser=discover_local_args_parser)
                add_command_args(parser=discover_local_args_parser)

                original_config_args_parsed, _ = orginal_args_parser.parse_known_args(
                    args=args_in
                )

                discover_local_args_parsed = discover_local_args_parser.parse_args(
                    discover_local_args, namespace=original_config_args_parsed
                )

                uids = await self._send_to_devices(
                    discover_local_args_parsed,
                    args_in,
                    udp=udp,
                    tcp=tcp,
                    timeout_ms=3500,
                )
                if isinstance(uids, set) or isinstance(uids, list):
                    # args_in.extend(["--device_unitids", ",".join(list(uids))])
                    args_in = ["--device_unitids", ",".join(list(uids))] + args_in
                elif isinstance(uids, str) and uids == "no_devices":
                    return False
                else:
                    LOGGER.error("Error during local discovery of the devices.")
                    return False

                add_command_args(parser=orginal_args_parser)
                args = orginal_args_parser.parse_args(args=args_in, namespace=args)

            if args.device_name is not None:
                if not self.acc_settings:
                    LOGGER.error(
                        'Missing account settings to resolve device name  "'
                        + args.device_name
                        + '"to unit id.'
                    )
                    return 1
                dev: list[str] = [
                    format_uid(device["localDeviceId"])
                    for device in self.acc_settings["devices"]
                    if device["name"] == args.device_name
                ]
                if not dev:
                    LOGGER.error(
                        'Device name "'
                        + args.device_name
                        + '" not found in account settings.'
                    )
                    return 1
                else:
                    target_device_uids: set[str] = set(format_uid(dev[0]))

            if args.device_unitids is not None:
                target_device_uids = set(
                    map(format_uid, set(args.device_unitids[0].split(",")))
                )
                print("Send to device: " + ", ".join(args.device_unitids[0].split(",")))


            commands_to_send: list[str] = [i for i in commands_send_to_bulb if hasattr(args, i) and getattr(args, i)]

            if commands_to_send:
                print("Commands to send to devices: " + ", ".join(commands_to_send))
            else:
                print("Commands (arguments):")
                print(sep_width * "-")

                def get_temp_range(product_id):
                    temperature_enum = []
                    try:
                        temperature_enum = [
                            trait["value_schema"]["properties"]["colorTemperature"][
                                "enum"
                            ]
                            if "properties" in trait["value_schema"]
                            else trait["value_schema"]["enum"]
                            for trait in device_configs[product_id]["deviceTraits"]
                            if trait["trait"] == "@core/traits/color-temperature"
                        ]
                        if len(temperature_enum[0]) < 2:
                            raise Exception()
                    except:
                        return False
                    return temperature_enum[0]

                def get_inner_range(tup1, tup2) -> tuple[int, int]:
                    return (
                        tup1[0] if tup1[0] > tup2[0] else tup2[0],
                        tup1[1] if tup1[1] < tup2[1] else tup2[1],
                    )

                temperature_enum = []
                color: list[int] = [0, 255]
                brightness: list[int] = [0, 100]
                for u_id in args.device_unitids[0].split(","):
                    u_id: str = format_uid(u_id)
                    if u_id not in self.devices or not self.devices[u_id].ident:

                        async def send_ping() -> bool:
                            discover_local_args2: list[str] = ["--ping", "--device_unitids", u_id]

                            orginal_args_parser: ArgumentParser = get_description_parser()
                            discover_local_args_parser2: ArgumentParser = get_description_parser()

                            add_config_args(parser=orginal_args_parser)
                            add_config_args(parser=discover_local_args_parser2)
                            add_command_args(parser=discover_local_args_parser2)

                            (
                                original_config_args_parsed,
                                _,
                            ) = orginal_args_parser.parse_known_args(args=args_in)

                            discover_local_args_parsed2 = (
                                discover_local_args_parser2.parse_args(
                                    discover_local_args2,
                                    namespace=original_config_args_parsed,
                                )
                            )

                            ret = await self._send_to_devices(
                                discover_local_args_parsed2,
                                args_in,
                                udp=udp,
                                tcp=tcp,
                                timeout_ms=3000,
                            )
                            if isinstance(ret, bool) and ret:
                                return True
                            else:
                                return False

                        ret: bool = await send_ping()
                        if isinstance(ret, bool) and ret:
                            product_id: str = self.devices[u_id].ident.product_id
                        else:
                            LOGGER.error(f"Device {u_id} not found.")
                            return False
                    product_id = self.devices[u_id].ident.product_id
                    if not temperature_enum:
                        temperature_enum = get_temp_range(product_id)
                    else:
                        temperature_enum: tuple[int, int] = get_inner_range(
                            temperature_enum, get_temp_range(product_id)
                        )
                arguments_send_to_device = {}
                if temperature_enum:
                    arguments_send_to_device = {
                        "temperature": " ["
                        + str(temperature_enum[0])
                        + "-"
                        + str(temperature_enum[1])
                        + "] (Kelvin, low: warm, high: cold)"
                    }

                arguments_send_to_device: dict[str, str] = {
                    **arguments_send_to_device,
                    **{
                        "color": f" rgb [{color[0]}..{color[1]}] [{color[0]}..{color[1]}] [{color[0]}..{color[1]}]",
                        "brightness": " ["
                        + str(brightness[0])
                        + ".."
                        + str(brightness[1])
                        + "]",
                        "routine_commands": " [cmd]",
                        "routine_id": " [int]",
                        "power": " [on/off]",
                    },
                }

                count = 1
                for c in commands_send_to_bulb:
                    args_to_b: str = (
                        arguments_send_to_device[c] if c in arguments_send_to_device else ""
                    )
                    print(str(count) + ") " + c + args_to_b)
                    count: int = count + 1

                cmd_c_id: int = int(input("Choose command number [1-9]*: "))
                if cmd_c_id > 0 and cmd_c_id < count:
                    args_in.append("--" + commands_send_to_bulb[cmd_c_id - 1])
                else:
                    LOGGER.error("No such command id " + str(cmd_c_id) + " available.")
                    sys.exit(1)

                if commands_send_to_bulb[cmd_c_id - 1] in arguments_send_to_device:
                    args_app: str = input(
                        "Set arguments (multiple arguments space separated) for command [Enter]: "
                    )
                    if args_app:
                        args_in.extend(args_app.split(" "))

                parser: ArgumentParser = get_description_parser()

                add_config_args(parser=parser)
                add_command_args(parser=parser)

                args = parser.parse_args(args_in, namespace=args)
                # args.func(args)

            if args.aes is not None:
                AES_KEYs["all"] = bytes.fromhex(args.aes[0])

            def local_and_cloud_command_msg(json_msg, timeout) -> None:
                message_queue_tx_local.append((json.dumps(json_msg), timeout))
                message_queue_tx_command_cloud.append(json_msg)

            if args.ota is not None:
                local_and_cloud_command_msg(
                    ({"type": "fw_update", "url": args.ota}, 10000)
                )

            if args.ping:
                local_and_cloud_command_msg({"type": "ping"}, 10000)

            if args.request:
                local_and_cloud_command_msg({"type": "request"}, 10000)

            if args.enable_tb is not None:
                a = args.enable_tb[0]
                if a != "yes" and a != "no":
                    print("ERROR --enable_tb needs to be yes or no")
                    sys.exit(1)

                message_queue_tx_local.append(
                    (json.dumps({"type": "backend", "link_enabled": a}), 1000)
                )

            if args.passive:
                pass

            if args.power:
                message_queue_tx_local.append(
                    (json.dumps({"type": "request", "status": args.power[0]}), 500)
                )
                message_queue_tx_state_cloud.append({"status": args.power[0]})

            if not args.selectDevice:
                product_ids: set[str] = {
                    device.ident.product_id
                    for uid, device in self.devices.items()
                    if device.ident and device.ident.product_id
                }

                for product_id in list(product_ids):
                    if product_id in device_configs:
                        continue
                    LOGGER.debug("Try to request device config from server.")
                    try:
                        config = await self.request(
                            "config/product/" + product_id,
                            timeout=30,
                        )
                        device_config: Device_config = config
                        device_configs[product_id] = device_config
                    except:
                        pass

            def forced_continue(reason: str) -> bool:
                if not args.force:
                    LOGGER.error(reason)
                    return False
                else:
                    LOGGER.info(reason)
                    LOGGER.info("Enforced send")
                    return True

            """range"""
            Check_device_parameter = Enum(
                "Check_device_parameter", "color brightness temperature scene"
            )

            def missing_config(product_id) -> bool:
                if not forced_continue(
                    "Missing or faulty config values for device "
                    + " product_id: "
                    + product_id
                ):
                    return True
                return False

            #### Needing config profile versions implementation for checking trait ranges ###

            def check_color_range(product_id, values) -> bool:
                color_enum = []
                try:
                    # # different device trait schematics. for now go typical range
                    # color_enum = [
                    #     trait["value_schema"]["definitions"]["color_value"]
                    #     for trait in device_configs[product_id]["deviceTraits"]
                    #     if trait["trait"] == "@core/traits/color"
                    # ]
                    # color_range = (
                    #     color_enum[0]["minimum"],
                    #     color_enum[0]["maximum"],
                    # )
                    color_range = (
                        0,
                        255,
                    )
                    for value in values:
                        if int(value) < color_range[0] or int(value) > color_range[1]:
                            return forced_continue(
                                f"Color {value} out of range [{color_range[0]}..{color_range[1]}]."
                            )

                except:
                    return not missing_config(product_id)
                return True

            def check_brightness_range(product_id, value) -> bool:
                brightness_enum = []
                try:
                    # different device trait schematics. for now go typical range
                    # brightness_enum = [
                    #     trait["value_schema"]["properties"]["brightness"]
                    #     for trait in device_configs[product_id]["deviceTraits"]
                    #     if trait["trait"] == "@core/traits/brightness"
                    # ]
                    # brightness_range = (
                    #     brightness_enum[0]["minimum"],
                    #     brightness_enum[0]["maximum"],
                    # )
                    brightness_range = (
                        0,
                        100,
                    )

                    if (
                        int(value) < brightness_range[0]
                        or int(value) > brightness_range[1]
                    ):
                        return forced_continue(
                            f"Brightness {value} out of range [{brightness_range[0]}..{brightness_range[1]}]."
                        )

                except:
                    return not missing_config(product_id)
                return True

            def check_temp_range(product_id, value) -> bool:
                temperature_range: list[int] = []
                try:
                    # # different device trait schematics. for now go typical range
                    # temperature_range = [
                    #     trait["value_schema"]["properties"]["colorTemperature"]["enum"]
                    #     if "properties" in trait["value_schema"]
                    #     else trait["value_schema"]["enum"]
                    #     for trait in device_configs[product_id]["deviceTraits"]
                    #     if trait["trait"] == "@core/traits/color-temperature"
                    # ][0]
                    temperature_range = [2000, 6500]
                    if (
                        int(value) < temperature_range[0]
                        or int(value) > temperature_range[1]
                    ):
                        return forced_continue(
                            f"Temperature {value} out of range [{temperature_range[0]}..{temperature_range[1]}]."
                        )
                except Exception as excp:
                    return not missing_config(product_id)
                return True

            def check_scene_support(product_id, scene) -> bool:
                color_enum = []
                try:
                    # color_enum = [
                    #     trait
                    #     for trait in device_configs[product_id]["deviceTraits"]
                    #     if trait["trait"] == "@core/traits/color"
                    # ]
                    # color_support = len(color_enum) > 0

                    # if not color_support and not "cwww" in scene:
                    #     return forced_continue(
                    #         f"Scene {scene['label']} not supported by device product {product_id}."
                    #     )
                    return True

                except:
                    return not missing_config(product_id)
                return True

            check_range = {
                Check_device_parameter.color: check_color_range,
                Check_device_parameter.brightness: check_brightness_range,
                Check_device_parameter.temperature: check_temp_range,
                Check_device_parameter.scene: check_scene_support,
            }

            def check_device_parameter(
                parameter: Check_device_parameter, values, product_id
            ) -> bool:
                # if not device_configs and not forced_continue("Missing configs for devices."):
                #     return False

                # for u_id in target_device_uids:
                #     # dev = [
                #     #     device["productId"]
                #     #     for device in self.acc_settings["devices"]
                #     #     if format_uid(device["localDeviceId"]) == format_uid(u_id)
                #     # ]
                #     # product_id = dev[0]
                #     product_id = self.devices[u_id].ident.product_id

                if not check_range[parameter](product_id, values):
                    return False
                return True

            if args.color is not None:
                r, g, b = args.color
                # if not check_device_parameter(Check_device_parameter.color, [r, g, b]):
                #     return False

                tt = args.transitionTime[0]
                msg = color_message(
                    r, g, b, int(tt), skipWait=args.brightness is not None
                )

                check_color = functools.partial(
                    check_device_parameter, Check_device_parameter.color, [r, g, b]
                )
                msg = msg + (check_color,)

                message_queue_tx_local.append(msg)
                col = json.loads(msg[0])["color"]
                message_queue_tx_state_cloud.append({"color": col})

            if args.temperature is not None:
                temperature = args.temperature[0]
                # if not check_device_parameter(Check_device_parameter.temperature, temperature):
                #     return False

                tt = args.transitionTime[0]
                msg = temperature_message(
                    temperature, int(tt), skipWait=args.brightness is not None
                )

                check_temperature = functools.partial(
                    check_device_parameter, Check_device_parameter.temperature, temperature
                )
                msg = msg + (check_temperature,)

                temperature = json.loads(msg[0])["temperature"]
                message_queue_tx_local.append(msg)
                message_queue_tx_state_cloud.append({"temperature": temperature})

            if args.brightness is not None:
                brightness = args.brightness[0]
                # if not check_device_parameter(Check_device_parameter.brightness, brightness):
                #     return False

                tt = args.transitionTime[0]
                msg: tuple[str, int] = brightness_message(brightness, int(tt))

                check_brightness = functools.partial(
                    check_device_parameter, Check_device_parameter.brightness, brightness
                )
                msg = msg + (check_brightness,)

                message_queue_tx_local.append(msg)
                brightness = json.loads(msg[0])["brightness"]
                message_queue_tx_state_cloud.append({"brightness": brightness})

            if args.percent_color is not None:
                if not device_configs and not forced_continue(
                    "Missing configs for devices."
                ):
                    return False
                r, g, b, w, c = args.percent_color
                tt = args.transitionTime[0]
                msg = percent_color_message(
                    r, g, b, w, c, int(tt), skipWait=args.brightness is not None
                )
                message_queue_tx_local.append(msg)
                p_color = json.loads(msg[0])["p_color"]
                message_queue_tx_state_cloud.append({"p_color": p_color})

            if args.factory_reset:
                local_and_cloud_command_msg({"type": "factory_reset"}, 500)

            if args.fade is not None and len(args.fade) == 2:
                local_and_cloud_command_msg({"type": "request","fade_out": args.fade[1],"fade_in": args.fade[0]}, 500)

            scene = ""
            if args.WW:
                scene = "Warm White"
            if args.daylight:
                scene = "Daylight"
            if args.CW:
                scene = "Cold White"
            if args.nightlight:
                scene = "Night Light"
            if args.relax:
                scene = "Relax"
            if args.TVtime:
                scene = "TV time"
            if args.comfort:
                scene = "Comfort"
            if args.focused:
                scene = "Focused"
            if args.fireplace:
                scene = "Fireplace"
            if args.club:
                scene = "Jazz Club"
            if args.romantic:
                scene = "Romantic"
            if args.gentle:
                scene = "Gentle"
            if args.summer:
                scene = "Summer"
            if args.jungle:
                scene = "Jungle"
            if args.ocean:
                scene = "Ocean"
            if args.fall:  # Autumn
                scene = "Fall"
            if args.sunset:
                scene = "Sunset"
            if args.party:
                scene = "Party"
            if args.spring:
                scene = "Spring"
            if args.forest:
                scene = "Forest"
            if args.deep_sea:
                scene = "Deep Sea"
            if args.tropical:
                scene = "Tropical"
            if args.magic:
                scene = "Magic Mood"
            if args.mystic:
                scene = "Mystic Mountain"
            if args.cotton:
                scene = "Cotton Candy"
            if args.ice:
                scene = "Ice Cream"

            # if (
            #     args.WW
            #     or args.daylight
            #     or args.CW
            #     or args.nightlight
            #     or args.relax
            #     or args.TVtime
            #     or args.comfort
            #     or args.focused
            #     or args.fireplace
            #     or args.club
            #     or args.romantic
            #     or args.gentle
            #     or args.summer
            #     or args.jungle
            #     or args.ocean
            #     or args.fall  # Autumn
            #     or args.sunset
            #     or args.party
            #     or args.spring
            #     or args.forest
            #     or args.deep_sea
            #     or args.tropical
            #     or args.magic
            #     or args.mystic
            #     or args.cotton
            #     or args.ice
            #     # or args.monjito
            # ):
            if scene:
                scene_result = [x for x in BULB_SCENES if x["label"] == scene]
                if not len(scene_result) or len(scene_result) > 1:
                    LOGGER.error(
                        f"Scene {scene} not found or more than one scene with the name found."
                    )
                    return False
                scene_obj = scene_result[0]

                # check_brightness = functools.partial(check_device_parameter, Check_device_parameter.scene, scene_obj)
                # msg = msg + (check_brightness,)
                # if not check_device_parameter(Check_device_parameter.scene, scene_obj):
                #     return False
                commands = scene_obj["commands"]
                if len(commands.split(";")) > 2:
                    commands += "l 0;"
                args.routine_id = 0
                args.routine_put = True
                args.routine_commands = commands
                args.routine_scene = str(scene_obj["id"])

            if args.routine_list:
                local_and_cloud_command_msg({"type": "routine", "action": "list"}, 500)

            if args.routine_put and args.routine_id is not None:
                local_and_cloud_command_msg(
                    {
                        "type": "routine",
                        "action": "put",
                        "id": args.routine_id,
                        "scene": args.routine_scene,
                        "commands": args.routine_commands,
                    },
                    500,
                )

            if args.routine_delete and args.routine_id is not None:
                local_and_cloud_command_msg(
                    {"type": "routine", "action": "delete", "id": args.routine_id}, 500
                )
            if args.routine_start and args.routine_id is not None:
                local_and_cloud_command_msg(
                    {"type": "routine", "action": "start", "id": args.routine_id}, 500
                )

            if args.reboot:
                local_and_cloud_command_msg({"type": "reboot"}, 500)

            if args.command is not None:
                if args.command == "get":
                    get_dict: dict[str, Any] = {"type":"request", "action":"get",}
                    if args.power or args.all:
                        get_dict["power"] = None
                    if args.cleaning or args.all:
                        get_dict["cleaning"] = None
                    if args.beeping or args.all:
                        get_dict["beeping"] = None
                    if args.battery or args.all:
                        get_dict["battery"] = None
                    if args.sidebrush or args.all:
                        get_dict["sidebrush"] = None
                    if args.rollingbrush or args.all:
                        get_dict["rollingbrush"] = None
                    if args.filter or args.all:
                        get_dict["filter"] = None
                    if args.carpetbooster or args.all:
                        get_dict["carpetbooster"] = None
                    if args.area or args.all:
                        get_dict["area"] = None
                    if args.time or args.all:
                        get_dict["time"] = None
                    if args.calibrationtime or args.all:
                        get_dict["calibrationtime"] = None
                    if args.workingmode or args.all:
                        get_dict["workingmode"] = None
                    if args.workingstatus or args.all:
                        get_dict["workingstatus"] = None
                    if args.suction or args.all:
                        get_dict["suction"] = None
                    if args.water or args.all:
                        get_dict["water"] = None
                    if args.direction or args.all:
                        get_dict["direction"] = None
                    if args.errors or args.all:
                        get_dict["errors"] = None
                    if args.cleaningrec or args.all:
                        get_dict["cleaningrec"] = None
                    if args.equipmentmodel or args.all:
                        get_dict["equipmentmodel"] = None
                    if args.alarmmessages or args.all:
                        get_dict["alarmmessages"] = None
                    if args.commissioninfo or args.all:
                        get_dict["commissioninfo"] = None
                    if args.mcu or args.all:
                        get_dict["mcu"] = None
                    local_and_cloud_command_msg(get_dict, 1000)

                elif args.command == "set":
                    set_dict: dict[str, Any] = {"type":"request", "action":"set"}
                    if args.power is not None:
                        set_dict["power"] = args.power
                    if args.cleaning is not None:
                        set_dict["cleaning"] = args.cleaning
                    if args.beeping is not None:
                        set_dict["beeping"] = args.beeping
                    if args.carpetbooster is not None:
                        set_dict["carpetbooster"] = args.carpetbooster
                    if args.workingmode is not None:
                        mode: int = VC_WORKINGMODE[args.workingmode].value
                        set_dict["workingmode"] = mode
                    if args.suction is not None:
                        suction: int = VC_SUCTION_STRENGTHS[args.suction].value
                        set_dict["suction"] = suction - 1
                    if args.water is not None:
                        set_dict["water"] = args.water
                    if args.direction is not None:
                        set_dict["direction"] = args.direction
                    if args.commissioninfo is not None:
                        set_dict["commissioninfo"] = args.commissioninfo
                    if args.calibrationtime is not None:
                        set_dict["calibrationtime"] = args.calibrationtime
                    local_and_cloud_command_msg(set_dict, 1000)

                elif args.command == "reset":
                    reset_dict: dict[str, Any] = { "type" : "request","action": "reset"}
                    if args.sidebrush:
                        reset_dict["sidebrush"] = None
                    if args.rollingbrush:
                        reset_dict["rollingbrush"] = None
                    if args.filter:
                        reset_dict["filter"] = None
                    local_and_cloud_command_msg(reset_dict, 1000)

            success = True
            if args.local or args.tryLocalThanCloud:
                if args.passive:
                    LOGGER.debug("Waiting for UDP broadcast")
                    data, address = udp.recvfrom(4096)
                    LOGGER.debug(
                        "\n\n 2. UDP server received: ",
                        data.decode("utf-8"),
                        "from",
                        address,
                        "\n\n",
                    )

                    LOGGER.debug("3a. Sending UDP ack.\n")
                    udp.sendto("QCX-ACK".encode("utf-8"), address)
                    time.sleep(1)
                    LOGGER.debug("3b. Sending UDP ack.\n")
                    udp.sendto("QCX-ACK".encode("utf-8"), address)
                else:

                    message_queue_tx_local.reverse()
                    send_started_local: datetime.datetime = datetime.datetime.now()

                    if args.discover:

                        print(sep_width * "-")
                        print("Search local network for devices ...")
                        print(sep_width * "-")

                        discover_end_event: Event = asyncio.Event()
                        discover_timeout_secs: float = 2.5

                        async def discover_answer_end(answer: TypeJSON, uid: str) -> None:
                            LOGGER.debug(f"discover ping end")
                            discover_end_event.set()

                        LOGGER.debug(f"discover ping start")
                        # send a message to uid "all" which is fake but will get the identification message
                        # from the devices in the aes_search and send msg function and we can send then a real
                        # request message to these discovered devices.
                        await self.set_send_message(
                            message_queue_tx_local,
                            "all",
                            args,
                            discover_answer_end,
                            discover_timeout_secs,
                        )

                        await discover_end_event.wait()
                        if self.devices:
                            target_device_uids = set(
                                u_id for u_id, v in self.devices.items()
                            )
                    # else:
                    msg_wait_tasks = {}

                    to_send_device_uids: set[str] = target_device_uids.copy()

                    async def sl(uid) -> None:
                        try:
                            await asyncio.sleep(timeout_ms / 1000)
                        except CancelledError as e:
                            LOGGER.debug(f"sleep uid {uid} cancelled.")
                        except Exception as e:
                            pass

                    for i in target_device_uids:
                        try:
                            msg_wait_tasks[i] = loop.create_task(sl(i))
                        except Exception as e:
                            pass

                    async def async_answer_callback_local(msg, uid) -> None:
                        if msg and msg.msg_queue_sent:
                            LOGGER.debug(f"{uid} msg callback.")
                        # else:
                        #     LOGGER.debug(f"{uid} {msg} msg callback.")
                        if uid in to_send_device_uids:
                            to_send_device_uids.remove(uid)
                        try:
                            msg_wait_tasks[uid].cancel()
                        except:
                            pass
                        if async_answer_callback:
                            await async_answer_callback(msg, uid)

                    for i in target_device_uids:
                        await self.set_send_message(
                            message_queue_tx_local.copy(),
                            i,
                            args,
                            callback=async_answer_callback_local,
                            time_to_live_secs=(timeout_ms / 1000),
                        )

                    for i in target_device_uids:
                        try:
                            LOGGER.debug(f"wait for send task {i}.")
                            await asyncio.wait([msg_wait_tasks[i]])
                            LOGGER.debug(f"wait for send task {i} end.")
                            # await asyncio.wait_for(msg_wait_tasks[i], timeout=(timeout_ms / 1000))
                        except CancelledError as e:
                            LOGGER.debug(f"sleep wait for uid {i} cancelled.")
                        except Exception as e:
                            pass

                    LOGGER.debug(f"wait for all target device uids done.")

                    if args.selectDevice:
                        print(sep_width * "-")
                        # devices_working = {k: v for k, v in self.devices.items() if v.local.aes_key_confirmed}
                        devices_working: dict[str, KlyqaDevice] = {
                            u_id: device
                            for u_id, device in self.devices.items()
                            if (device.status and device.status.ts > send_started_local)
                            or (
                                (args.cloud or args.tryLocalThanCloud)
                                and device.cloud
                                and device.cloud.connected
                            )
                        }
                        print(
                            "Found "
                            + str(len(devices_working))
                            + " "
                            + ("device" if len(devices_working) == 1 else "devices")
                            + " with working aes keys"
                            + (" (dev aes key)" if args.dev else "")
                            + "."
                        )
                        if len(devices_working) <= 0:
                            return "no_devices"
                        print(sep_width * "-")
                        count = 1
                        device_items: list[KlyqaDevice] = list(devices_working.values())

                        if device_items:
                            print(
                                "Status attributes: ("
                                + get_obj_attrs_as_string(KlyqaBulbResponseStatus)
                                + ") (local IP-Address)"
                            )
                            print("")

                        for device in device_items:
                            name: str = f"Unit ID: {device.u_id}"
                            if device.acc_sets and "name" in device.acc_sets:
                                name = device.acc_sets["name"]
                            address: str = (
                                f" (local {device.local.address['ip']}:{device.local.address['port']})"
                                if device.local.address["ip"]
                                else ""
                            )
                            cloud = (
                                f" (cloud connected)" if device.cloud.connected else ""
                            )
                            status: str = (
                                f" ({device.status})" if device.status else " (no status)"
                            )
                            print(f"{count}) {name}{status}{address}{cloud}")
                            count = count + 1

                        if self.devices:
                            print("")
                            device_num_s: str = input(
                                "Choose bulb number(s) (comma seperated) a (all),[1-9]*{,[1-9]*}*: "
                            )
                            target_device_uids_lcl = set()
                            if device_num_s == "a":
                                return set(b.u_id for b in device_items)
                            else:
                                for bulb_num in device_num_s.split(","):
                                    bulb_num: int = int(bulb_num)
                                    if bulb_num > 0 and bulb_num < count:
                                        target_device_uids_lcl.add(
                                            device_items[bulb_num - 1].u_id
                                        )
                            return target_device_uids_lcl

                        """ no devices found. Exit script. """
                        sys.exit(0)

                if target_device_uids and len(to_send_device_uids) > 0:
                    """error"""
                    sent_locally_error: str = (
                        "The commands "
                        + "failed to send locally to the device(s): "
                        + ", ".join(to_send_device_uids)
                    )
                    if args.tryLocalThanCloud:
                        LOGGER.info(sent_locally_error)
                    else:
                        LOGGER.error(sent_locally_error)
                    success = False

            if args.cloud or args.tryLocalThanCloud:
                """cloud processing"""

                queue_printer: EventQueuePrinter = EventQueuePrinter()
                response_queue = []

                async def _cloud_post(device: KlyqaDevice, json_message, target: str) -> None:
                    cloud_device_id = device.acc_sets["cloudDeviceId"]
                    unit_id: str = format_uid(device.acc_sets["localDeviceId"])
                    LOGGER.info(
                        f"Post {target} to the device '{cloud_device_id}' (unit_id: {unit_id}) over the cloud."
                    )
                    resp = {
                        cloud_device_id: await self.post(
                            url=f"device/{cloud_device_id}/{target}",
                            json=json_message,
                        )
                    }
                    resp_print = ""
                    name: str = device.u_id
                    if device.acc_sets and "name" in device.acc_sets:
                        name = device.acc_sets["name"]
                    resp_print: str = f'Device "{name}" cloud response:'
                    resp_print = json.dumps(resp, sort_keys=True, indent=4)
                    device.cloud.received_packages.append(resp)
                    response_queue.append(resp_print)
                    queue_printer.print(resp_print)

                async def cloud_post(device: KlyqaDevice, json_message, target: str):
                    if not await device.use_lock():
                        LOGGER.error(
                            f"Couldn't get use lock for device {device.get_name()})"
                        )
                        return 1
                    try:
                        await _cloud_post(device, json_message, target)
                    except CancelledError:
                        LOGGER.error(
                            f"Cancelled cloud send "
                            + (device.u_id if device.u_id else "")
                            + "."
                        )
                    finally:
                        await device.use_unlock()

                started: datetime.datetime = datetime.datetime.now()
                # timeout_ms = 30000

                async def process_cloud_messages(target_uids) -> None:

                    threads = []
                    target_devices: list[KlyqaDevice] = [
                        b
                        for b in self.devices.values()
                        for t in target_uids
                        if b.u_id == t
                    ]

                    def create_post_threads(target, msg):
                        return [
                            (loop.create_task(cloud_post(b, msg, target)), b)
                            for b in target_devices
                        ]

                    state_payload_message = dict(
                        ChainMap(*message_queue_tx_state_cloud)
                    )
                    # state_payload_message = json.loads(*message_queue_tx_state_cloud) if message_queue_tx_state_cloud else ""

                    command_payload_message = dict(
                        ChainMap(*message_queue_tx_command_cloud)
                    )
                    # command_payload_message = json.loads(*message_queue_tx_command_cloud) if message_queue_tx_command_cloud else ""
                    if state_payload_message:
                        threads.extend(
                            create_post_threads(
                                "state", {"payload": state_payload_message}
                            )
                        )
                    if command_payload_message:
                        threads.extend(
                            create_post_threads("command", command_payload_message)
                        )

                    count = 0
                    timeout: float = timeout_ms / 1000
                    for t, device in threads:
                        count: int = count + 1
                        """wait at most timeout_ms wanted minus seconds elapsed since sending"""
                        try:
                            await asyncio.wait_for(
                                t,
                                timeout=timeout
                                - (datetime.datetime.now() - started).seconds,
                            )
                        except asyncio.TimeoutError:
                            LOGGER.error(f'Timeout for "{device.get_name()}"!')
                            t.cancel()
                        except:
                            pass

                await process_cloud_messages(
                    target_device_uids if args.cloud else to_send_device_uids
                )
                """if there are still target devices that the local send couldn't reach, try send the to_send_device_uids via cloud"""

                queue_printer.stop()

                if len(response_queue):
                    success = True

            if success and scene:
                scene_start_args: list[str] = ["--routine_id", "0", "--routine_start"]

                orginal_args_parser = get_description_parser()
                scene_start_args_parser: ArgumentParser = get_description_parser()

                add_config_args(parser=orginal_args_parser)
                add_config_args(parser=scene_start_args_parser)
                add_command_args(parser=scene_start_args_parser)

                original_config_args_parsed, _ = orginal_args_parser.parse_known_args(
                    args=args_in
                )

                scene_start_args_parsed = scene_start_args_parser.parse_args(
                    scene_start_args, namespace=original_config_args_parsed
                )

                ret = await self._send_to_devices(
                    scene_start_args_parsed,
                    args_in,
                    udp=udp,
                    tcp=tcp,
                    timeout_ms=timeout_ms
                    - (datetime.datetime.now() - send_started).total_seconds()
                    * 1000,  # 3000
                )

                if isinstance(ret, bool) and ret:
                    success = True
                else:
                    LOGGER.error(f"Couldn't start scene {scene}.")
                    success = False

            return success
        except Exception as e:
            LOGGER.debug(traceback.format_exc())

    async def send_to_devices(self, args_parsed, args_in, timeout_ms=5000):
        """set up broadcast port and tcp reply connection port"""

        if args_parsed.cloud or args_parsed.local:
            args_parsed.tryLocalThanCloud = False

        if args_parsed.debug:
            LOGGER.setLevel(level=logging.DEBUG)
            logging_hdl.setLevel(level=logging.DEBUG)

        if args_parsed.dev:
            AES_KEYs["dev"] = AES_KEY_DEV

        local_communication = args_parsed.local or args_parsed.tryLocalThanCloud
        # self.data_communicator.udp = None
        # self.data_communicator.tcp = None

        if local_communication:
            # await tcp_udp_port_lock.acquire()
            if not await self.data_communicator.bind_ports(
                # args_parsed.myip[0] if args_parsed.myip is not None else None
            ):
                return 1
            # try:
            #     self.data_communicator.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #     self.data_communicator.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            #     self.data_communicator.udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #     if args_parsed.myip is not None:
            #         server_address = (args_parsed.myip[0], 2222)
            #     else:
            #         server_address = ("0.0.0.0", 2222)
            #     self.data_communicator.udp.bind(server_address)
            #     LOGGER.debug("Bound UDP port 2222")

            # except:
            #     LOGGER.error(
            #         "Error on opening and binding the udp port 2222 on host for initiating the device communication."
            #     )
            #     return 1

            # try:
            #     self.data_communicator.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     self.data_communicator.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #     server_address = ("0.0.0.0", 3333)
            #     self.data_communicator.tcp.bind(server_address)
            #     LOGGER.debug("Bound TCP port 3333")
            #     self.data_communicator.tcp.listen(1)

            # except:
            #     LOGGER.error(
            #         "Error on opening and binding the tcp port 3333 on host for initiating the device communication."
            #     )
            #     return 1

        exit_ret = 0

        async def async_answer_callback(msg, uid):
            print(f"{uid}: ")
            if msg:
                try:
                    LOGGER.info(f"Answer received from {uid}.")
                    print(
                        f"{json.dumps(json.loads(msg.answer), sort_keys=True, indent=4)}"
                    )
                except:
                    pass
            else:
                LOGGER.error(f"Error no message returned from {uid}.")

        if not await self._send_to_devices(
            args_parsed,
            args_in,
            udp=self.data_communicator.udp,
            tcp=self.data_communicator.tcp,
            timeout_ms=timeout_ms,
            async_answer_callback=async_answer_callback,
        ):
            exit_ret = 1

        # parser = get_description_parser()
        # args = ["--request"]
        # args.extend(["--local", "--debug", "--device_unitids", f"c4172283e5da92730bb5"])

        # add_config_args(parser=parser)
        # add_command_args(parser=parser)

        # args_parsed = parser.parse_args(args=args)

        # if not await self._send_to_devices(
        #     args_parsed, args, udp=self.data_communicator.udp, tcp=self.data_communicator.tcp, timeout_ms=timeout_ms, async_answer_callback=async_answer_callback
        # ):
        #     exit_ret = 1

        await self.search_and_send_loop_task_stop()

        LOGGER.debug("Closing ports")
        if local_communication:
            self.data_communicator.shutdown()
            # try:
            #     self.data_communicator.tcp.shutdown(socket.SHUT_RDWR)
            #     self.data_communicator.tcp.close()
            #     LOGGER.debug("Closed TCP port 3333")
            # except:
            #     pass

            # try:
            #     self.udp.close()
            #     LOGGER.debug("Closed UDP port 2222")
            # except:
            #     pass
            # tcp_udp_port_lock.release()

        return exit_ret


def main():
    # global klyqa_accs

    klyqa_accs: dict[str, Klyqa_account] = None
    if not klyqa_accs:
        klyqa_accs = dict()

    loop = asyncio.get_event_loop()

    parser = get_description_parser()

    add_config_args(parser=parser)

    add_command_args(parser=parser)
    args_in: list[str] = sys.argv[1:]

    if len(args_in) < 2:
        parser.print_help()
        sys.exit(1)

    args_parsed = parser.parse_args(args=args_in)

    if not args_parsed:
        sys.exit(1)

    if args_parsed.debug:
        LOGGER.setLevel(level=logging.DEBUG)
        logging_hdl.setLevel(level=logging.DEBUG)

    server_ip = args_parsed.myip[0] if args_parsed.myip else "0.0.0.0"
    data_communicator: Data_communicator = Data_communicator(server_ip)

    # loop.run_until_complete(data_communicator.bind_ports())

    print_onboarded_devices: bool = (
        not args_parsed.device_name
        and not args_parsed.device_unitids
        and not args_parsed.allDevices
    )

    klyqa_acc: Klyqa_account = None

    if args_parsed.dev or args_parsed.aes:
        if args_parsed.dev:
            LOGGER.info("development mode. Using default aes key.")
        elif args_parsed.aes:
            LOGGER.info("aes key passed.")
        klyqa_acc = Klyqa_account(data_communicator)

    elif args_parsed.username is not None and args_parsed.username[0] in klyqa_accs:

        klyqa_acc = klyqa_accs[args_parsed.username[0]]
        if not klyqa_acc.access_token:
            asyncio.run(klyqa_acc.login(print_onboarded_devices=print_onboarded_devices))
            LOGGER.debug("login finished")

    else:
        try:
            LOGGER.debug("login")
            host = PROD_HOST
            if args_parsed.test:
                host = TEST_HOST
            klyqa_acc = Klyqa_account(
                data_communicator,
                args_parsed.username[0] if args_parsed.username else "",
                args_parsed.password[0] if args_parsed.password else "",
                host,
            )

            asyncio.run(klyqa_acc.login(print_onboarded_devices=print_onboarded_devices))
            klyqa_accs[args_parsed.username[0]] = klyqa_acc
        except:
            LOGGER.error("Error during login.")
            sys.exit(1)

        LOGGER.debug("login finished")
    exit_ret = 0

    if (
        loop.run_until_complete(
            klyqa_acc.send_to_devices(
                args_parsed, args_in.copy(), timeout_ms=DEFAULT_SEND_TIMEOUT_MS
            )
        )
        > 0
    ):
        exit_ret = 1

    klyqa_acc.shutdown()

    sys.exit(exit_ret)


if __name__ == "__main__":
    main()
