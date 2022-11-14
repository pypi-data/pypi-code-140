# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

from .base import ConfigStoreBase, ConfigurationNotFound


class RedisStore(ConfigStoreBase):
    __slots__ = ["parser", "redis"]

    def __init__(self, parser, arguments):
        """Initialize the Redis configuration store

        :param parser: Configuration file/data parser
        :type parser: minty.config.parser.Base
        :param redis: dictionary containing keys/values to configure a Redis
            client instance.
        :type arguments: dict
        """

        self.parser = parser
        self.redis = arguments

    def retrieve(self, name) -> str:
        """Retrieve configuration from Redis

        :param name: Name of the configuration to retrieve
        :param name: str
        :raises ConfigurationNotFound: if the named configuration can't be found
        :return: The configuration "file" contents
        :rtype: str
        """

        super().retrieve(name)

        timer = self.statsd.get_timer("config_database_read_duration")
        with timer.time():
            config = self.redis.get("saas:instance:" + name)
        self.statsd.get_counter("config_database_read_number").increment()

        if config is None:
            raise ConfigurationNotFound

        parsed = self.parser.parse(config.decode("utf-8"))

        return parsed["instance"]
