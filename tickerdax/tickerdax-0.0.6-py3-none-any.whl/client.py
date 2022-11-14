import os
import json
import sys
import asyncio
import requests
import tempfile
import logging
import redis
import docker
import socket
import websockets
from websockets.exceptions import InvalidStatusCode
from tickerdax.constants import Envs, KeyTypes, NAME
from docker.errors import DockerException
from datetime import datetime, timedelta, timezone
from tickerdax import formatting
from pprint import pformat, pprint
logging.basicConfig(level=logging.INFO)


class TickerDax:
    def __init__(self, email=None, rest_api_key=None, websocket_api_key=None, fast_start=True, connect=True):
        websocket_api_prefix = 'ws'
        rest_api_prefix = 'api'
        if os.environ.get(Envs.DEV):
            rest_api_prefix = 'dev-api'
            websocket_api_prefix = 'dev-ws'

        # general configuration
        self.supported_timeframes = ['1h']
        self.rest_values = []
        self.cached_values = []
        self.missing_values = []
        self._batch_size = 100
        self._fast_start = fast_start

        # rest api configuration
        self._rest_api_host = f'https://{rest_api_prefix}.{NAME}.com'
        self._rest_api_version = 'v1'
        self._rest_api_key = os.environ.get(Envs.REST_API_KEY, rest_api_key)

        # websocket api configuration
        self._host = f'wss://{websocket_api_prefix}.{NAME}.com'
        self._email = os.environ.get(Envs.EMAIL, email)
        self._websocket_api_key = os.environ.get(Envs.WEBSOCKET_API_KEY, websocket_api_key)

        # redis configuration
        self._redis_image = 'redis:7-alpine3.16'
        self._redis_server_address = os.environ.get(Envs.REDIS_SERVER_ADDRESS, '127.0.0.1')
        self._redis_container_name = f'{NAME}-redis'
        self._redis_container_port = os.environ.get(Envs.REDIS_SERVER_PORT, 6379)
        self._redis_host_port = os.environ.get(Envs.REDIS_SERVER_PORT, 6379)

        # clients
        self._docker_client = None
        self._redis_client = None

        self._cache_folder = os.path.join(os.environ.get(Envs.CACHE_ROOT, tempfile.gettempdir()), f'{NAME}_cache')
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(level=logging.DEBUG)

        if connect:
            self._start_redis_server()

    @staticmethod
    def _get_cache_keys(route, symbols, timestamps):
        """
        Get all the cache keys.

        :param str route: The data route.
        :param list[str] symbols: A list of symbols.
        :param list[float] timestamps: The timestamps to get.
        :returns: A complete list of all the cache keys.
        :rtype list
        """
        keys = []
        for symbol in symbols:
            keys.extend([f'{NAME}/{route}/{symbol}/{timestamp}' for timestamp in timestamps])
        return keys

    @staticmethod
    def _format_route(route):
        """
        Normalizes the route format.

        :param str route: The data route.
        :returns: A normalizedd the route.
        :rtype str
        """
        return route.strip('/').strip('\\').replace('\\', '/')

    def _get_unused_port_number(self, default_port) -> int:
        """
        Gets an unused port number from the OS.

        :returns: A port number.
        :rtype: int
        """
        if not self._is_port_in_use(default_port):
            return default_port
        else:
            sock = socket.socket()
            sock.bind(('', 0))
            return sock.getsockname()[1]

    def _get_from_cache(self, keys):
        """
        Get the data from the cache that already exists, and which REST requests still need to be made.

        :param list[str] keys: A complete list of all the cache keys.
        :returns: A tuple of the cache values and which REST requests still need to be made.
        :rtype tuple(list, dict)
        """
        cache_values = self._redis_client.mget(keys)

        rest_requests = {}
        for key, cache_value in zip(keys, cache_values):
            if not cache_value:
                items = key.split('/')
                symbol = items[-2]
                timestamp = float(items[-1])

                if not rest_requests.get(symbol):
                    rest_requests[symbol] = []
                rest_requests[symbol].append(timestamp)

        # load the json data from the cached values and filter out None values
        cache_values = [json.loads(cache_value) for cache_value in cache_values if cache_value]

        # return the cached values and the needed rest requests
        return cache_values, rest_requests

    def _set_redis_client(self):
        """
        Sets the redis client.
        """
        # verify the connection with the redis server
        try:
            self._redis_client = redis.Redis(
                host=self._redis_server_address,
                port=self._redis_host_port,
                db=0
            )
            self._redis_client.ping()
            self._logger.info(f'Redis server is connected!')
            return True
        except redis.exceptions.ConnectionError:
            return False

    def _is_port_in_use(self, port: int) -> bool:
        """
        Checks if port number is in use.

        :param int port: A port number.
        :returns: Whether the port is in use.
        :rtype: bool
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
            return stream.connect_ex((self._redis_server_address, port)) == 0

    def _start_redis_server(self) -> None:
        """
        Starts the redis docker container.
        """
        # quickly try to connect to the running redis server
        if self._fast_start:
            if self._set_redis_client():
                return
            else:
                self._logger.warning(f'Failed to connect with fast start. Starting full reboot...')

        # get a unused host port
        self._redis_host_port = self._get_unused_port_number(6379)

        # initialize the docker client
        try:
            self._docker_client = docker.from_env()
        except DockerException:
            self.report_error('Failed to connect to docker. Make sure docker is installed and currently running.')

        # stop any running redis docker containers first
        for container in self._docker_client.containers.list(all=True):
            if self._redis_container_name == container.name:
                if container.status == 'running':
                    self._logger.info(f'Stopping docker container "{self._redis_container_name}"')
                    container.stop()
                    container.wait()
                self._logger.info(f'Removing docker container "{self._redis_container_name}"')
                container.remove()

        # start the redis docker container
        self._logger.info(f'Starting docker container "{self._redis_container_name}"')
        self._docker_client.containers.run(
            name=self._redis_container_name,
            image=self._redis_image,
            ports={
                f'{self._redis_container_port}/tcp': (self._redis_server_address, self._redis_host_port)
            },
            volumes=[f'{self._cache_folder}:/data'],
            detach=True
        )

        # connect the redis client
        if not self._set_redis_client():
            raise ConnectionError('TickerDax failed to connect to the redis server')

    async def _batch_request(self, route, symbol, timestamps):
        """
        Batches requests until all timestamps are retrieved.

        :param str route: The data route.
        :param str symbol: The symbol to get.
        :param list[float] timestamps: The timestamps to get.
        :returns A list of all the responses to the request.
        :rtype list[dict]
        """
        result = []
        rest_requests = []
        batch = []
        number_of_timestamp = len(timestamps)
        for index, key in enumerate(timestamps, 1):
            batch.append(key)

            if index % self._batch_size == 0:
                self._logger.info(f'batch requesting {index}/{number_of_timestamp} "{route}/{symbol}" timestamps...')
                rest_requests.append(self._rest_request(route, symbol, batch))

                # clear the batch
                batch.clear()

        # get any remaining items in the last batch
        if batch:
            self._logger.info(
                f'batch requesting {number_of_timestamp}/{number_of_timestamp} "{route}/{symbol}" timestamps...'
            )
            rest_requests.append(self._rest_request(route, symbol, batch))

        # gather the rest request batches concurrently
        for response in await asyncio.gather(*rest_requests):
            result.extend(response)

        self._logger.debug(f'batch "{route}/{symbol}" requests complete!')
        return result

    async def _stream_to_cache(self, route, symbols):
        """
        Connects to the given route and its symbols and updates the
        cache as it receives new data.

        :param str route: The data route.
        :param list[str] symbols: A list of symbols.
        """
        uri = f'{self._host}?route={route}&symbols={symbols}'
        try:
            async with websockets.connect(
                    uri,
                    extra_headers={'email': self._email, 'token': self._websocket_api_key}
            ) as connected_socket:
                self._logger.info(f"> Connected to {uri}")
                while True:
                    data = json.loads(await connected_socket.recv())
                    symbol = data.get('symbol')
                    timestamp = data.get('id')
                    if symbol and timestamp:
                        for key in self._get_cache_keys(client._format_route(route), [symbol], [timestamp]):
                            self._redis_client.set(key, json.dumps(data))
                            self._logger.info(f'Cached: {pformat(data)}')

        except InvalidStatusCode as error:
            if error.status_code == 401:
                self.report_error(
                    'This email and API key combination are not authorized to connect to '
                    'the https://tickerdax.com websocket API. Please check you credentials.'
                )

    async def _rest_request(self, route, symbol, timestamps):
        """
        Preforms a single REST request.

        :param str route: The data route.
        :param str symbol: The symbol to get.
        :param list[float] timestamps: The timestamps to get.
        :return list[dict]: A list of dictionaries as the response to the request.
        """
        try:
            response = requests.get(
                f'{self._rest_api_host}/{self._rest_api_version}/{route}',
                headers={"x-api-key": self._rest_api_key},
                data=json.dumps({
                    'symbol': symbol,
                    'timestamps': timestamps
                })
            )
            if response.ok:
                return response.json()
            else:
                self._logger.error(response.text)
                return []
        except Exception as error:
            self._logger.error(error)
            return []

    async def _request(self, route, rest_requests):
        """
        A request to first the local cache, then to the REST API if data is missing in the
        cache.

        :param str route: The data route.
        :param dict rest_requests: A dictionary of symbols and timestamps.
        :return list[dict]: A list of dictionaries as the response to the request.
        """
        rest_values = []
        if rest_requests:
            self._logger.info(f'Requesting {route} data from REST API...')
            # gather the symbols concurrently
            for result in await asyncio.gather(*[
                self._batch_request(route, symbol, timestamps) for symbol, timestamps in rest_requests.items()
            ]):
                rest_values.extend(result)

        return rest_values

    async def _stream(self, routes):
        """
        Streams all given routes and their symbols concurrently.

        :param dict routes: A dictionary of route names and their symbols.
        """
        await asyncio.gather(*[
            self._stream_to_cache(f'/{self._format_route(route)}', ','.join(symbols)) for route, symbols in routes.items()
        ])

    def _update_cache(self, route, keys, timeframe):
        """
        Saves any new data from the response to the cache.

        :param str route: The data route.
        :param list[str] keys: A complete list of all the cache keys.
        :param str timeframe: The time interval.
        :returns: The combined result of cache values, rest values, and blank values.
        :rtype list
        """
        result = []
        # remove all the cache keys that already had a cached value
        for cached_value in self.cached_values:
            symbol = cached_value.get('symbol')
            timestamp = cached_value.get('id')
            keys.remove(f'{NAME}/{route}/{symbol}/{timestamp}')
        result.extend(self.cached_values)

        # cache the rest values
        for rest_value in self.rest_values:
            symbol = rest_value.get('symbol')
            timestamp = rest_value.get('id')
            key = f'{NAME}/{route}/{symbol}/{timestamp}'

            self._redis_client.set(key, json.dumps(rest_value))
            # remove all the cache keys now  that it is cached
            keys.remove(key)
        result.extend(self.rest_values)

        # if there are any remaining keys, then that means they were missing from the rest api
        for key in keys:
            items = key.split('/')
            symbol = items[-2]
            timestamp = float(items[-1])

            missing_value = {'id': timestamp, 'symbol': symbol}
            result.append(missing_value)

            # this will set the missing value in the cache with an expiration time that matches the given timeframe
            self.missing_values.append(missing_value)
            self._redis_client.set(
                key,
                json.dumps(missing_value),
                ex=formatting.convert_timeframe_to_seconds(timeframe)
            )
        return result

    def validate_api_key(self,  key_type):
        """
        Validate whether the key of the given type exists and show and error message.

        :param str key_type: The type of key i.e. REST or WEBSOCKET.
        """
        env_key_name = None
        if key_type == KeyTypes.REST and not self._rest_api_key:
            env_key_name = Envs.REST_API_KEY

        elif key_type == KeyTypes.WEBSOCKET and not self._websocket_api_key:
            env_key_name = Envs.WEBSOCKET_API_KEY

        if env_key_name:
            self.report_error(
                f'The environment variable "{env_key_name}" must set to your API key from https://tickerdax.com'
            )

    def get_available_routes(self):
        """
        Gets all available routes from the REST api.

        :returns: A list of all available routes from the REST api.
        :rtype: list
        """
        ignored_routes = ['info/usage-plans']
        routes = []
        for route in requests.get(f'{self._rest_api_host}/openapi.json').json().get('paths', {}).keys():
            route = route.strip(f'/{self._rest_api_version}/')
            if route not in ignored_routes:
                routes.append(route)
        return routes

    def get_route(self, route, symbols, start, end, timeframe='1h'):
        """
        Get data for a route and it's symbols between the start and end times and at the timeframe interval.

        :param str route: The data route.
        :param list[str] symbols: A list of symbols.
        :param datetime start: The UTC start time.
        :param datetime end: The UTC end time.
        :param str timeframe: The time interval.
        :returns: The sorted result.
        :rtype list
        """
        self.cached_values.clear()
        self.rest_values.clear()
        self.missing_values.clear()

        route = self._format_route(route)
        timestamps = formatting.get_timestamp_range(start, end, timeframe)
        keys = self._get_cache_keys(route, symbols, timestamps)

        # get the cached values and determine which rest requests are outstanding
        self._logger.debug(f'Checking "{route}" cache for {symbols}...')
        self.cached_values, outstanding_rest_requests = self._get_from_cache(keys)
        self.rest_values = asyncio.run(self._request(route, outstanding_rest_requests))

        result = self._update_cache(route, keys, timeframe)
        return sorted(result, key=lambda i: i['id'])

    def report_error(self, message):
        """
        Reports an error message to the user.

        :param str message: A error message.
        """
        self._logger.error(message)
        sys.exit(1)

    def stream(self, routes):
        """
        Streams all given routes and their symbols to the cache in real-time.

        :param dict routes: A dictionary of route names and their symbols.
        """
        try:
            asyncio.run(self._stream(routes))
        except Exception as error:
            self._logger.error(error)
            self._logger.info('Trying to reconnect...')
            asyncio.run(self._stream(routes))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = TickerDax()

    pprint(client.get_route(
        route='into-the-block/predictions',
        symbols=['BTC', 'LTC'],
        start=datetime.now(tz=timezone.utc) - timedelta(hours=6),
        end=datetime.now(tz=timezone.utc)
    ))

    client.stream(
        routes={
            'into-the-block/predictions': ['BTC', 'LTC'],
        },
    )
