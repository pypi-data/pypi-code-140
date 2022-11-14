import base64
import json
from collections import defaultdict
from itertools import chain
from typing import Any, List, Optional
from urllib.parse import urlparse

import django.urls.exceptions
import redis
import requests
from decouple import config
from melon_translate_client.utils.logging import log
from rest_framework.exceptions import ValidationError


class Client:
    """TranslateClient utils class."""

    CACHE_VIEW_TTL = config("CACHE_VIEW_TTL", default=2700, cast=int)
    CACHE_OCCURRENCE_TTL = config("CACHE_OCCURRENCE_TTL", default=2700, cast=int)
    CACHE_GROUP_KEY_TTL = config("CACHE_GROUP_KEY_TTL", default=2700, cast=int)

    timeout = config("REQUESTS_TIMEOUT", default=30, cast=int)

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        service_address: str = config(
            "TRANSLATE_ADDRESS", default="127.0.0.1", cast=str
        ),
        service_port: int = config("TRANSLATE_PORT", default=80, cast=int),
        cache_address: str = config("REDIS_HOST", default="127.0.0.1", cast=str),
        cache_port: int = config("REDIS_PORT", default=6379, cast=int),
    ):
        """
        Constructor method for melon-translate.Client class.

        :param service_address: Host address for melon-translate.
        :param service_port: Host port for melon-translate.
        :param cache_address: Host address for REDIS.
        :param cache_port: Host port for REDIS.
        """
        self.address = service_address
        self.port = service_port
        self.cache_address = cache_address
        self.cache_port = cache_port
        self.cache = redis.Redis(
            host=cache_address, port=cache_port, decode_responses=True
        )

    @staticmethod
    def __stringify(collection: List[Any]) -> List[str]:
        """Ensure items of a collection are stringified."""
        return [str(item) for item in collection]

    @staticmethod
    def __build_params(
        views: List[str],
        occurrences: List[str],
        snake_keys: List[str],
        page_size: int = None,
        page: int = None,
    ) -> dict:
        """Build HTTP params."""
        params = {}
        if views:
            params["view_name"] = views

        if occurrences:
            params["occurrences"] = occurrences

        if snake_keys:
            params["snake_keys"] = snake_keys

        if page_size and page:
            params["page_size"] = page_size
            params["page"] = page

        return params

    def __hash(self, *hashes) -> str:
        """Hash a collection."""
        return base64.b64encode(
            bytes(":".join(self.__stringify(hashes)), "utf-8")
        ).decode("utf-8")

    def __expire(self, *hashes: List[str]):
        """Expire given hash maps in cache."""
        for _hash in hashes:
            self.cache.expire(_hash, Client.CACHE_GROUP_KEY_TTL)

    def __set_view(self, language: str, view: str, ids: List[str]) -> Optional[bool]:
        """Set view with specified TTL."""
        return self.cache.set(
            f"{self.__hash(language, view)}",
            ",".join(self.__stringify(ids)),
            ex=Client.CACHE_VIEW_TTL,
        )

    def __set_occurrence(
        self, language: str, occurence: str, ids: List[str]
    ) -> Optional[bool]:
        """Set occurrence with specified TTL."""
        return self.cache.set(
            f"{self.__hash(language, occurence)}",
            ",".join(self.__stringify(ids)),
            ex=Client.CACHE_OCCURRENCE_TTL,
        )

    def __load_keys(self, keys: List[str]) -> dict:
        """Load keys from cache."""
        if isinstance(keys, str):
            keys = keys.split(",")

        _records = [json.loads(self.cache.get(key)) for key in keys]

        return {record.get("id"): record for record in _records}

    def snake_key(self, language: str, key: str) -> Optional[dict]:
        """Retrieve a snake key."""
        _SNAKE_NAME_MAP = f"{language}_snake_name"
        _VIEWS_ID_MAP = f"{language}_views"
        _OCCURRENCES_ID_MAP = f"{language}_occurrences"

        record_id = self.cache.hget(_SNAKE_NAME_MAP, key)
        if not record_id:
            log.warning(f"Key {key} could not be found.")
            raise RuntimeError(
                "missing translation - initialize translation with management command"
            )  # TODO: insert hook to re-initialize translations structure

        record = json.loads(self.cache.get(record_id))

        # NOTE: 1. Compute which views needs refreshing and refresh them and all associations.
        views = [
            view
            for view in record.get("views", [])
            if not self.cache.exists(self.__hash([language, view]))
        ]
        if views and not self.cache.hget(_VIEWS_ID_MAP, record_id):
            log.info(f"Caching views {views} for {language} language")
            _ = self.filter(language, views=views)

        # NOTE: 2. Compute which occurrences needs refreshing and refresh them and all associations.
        occurrences = [
            occurrence
            for occurrence in record.get("occurrences", [])
            if not self.cache.exists(self.__hash([language, occurrence]))
        ]
        if occurrences and not self.cache.hget(_OCCURRENCES_ID_MAP, record_id):
            log.info(f"Caching occurrences {occurrences} for {language} language")
            _ = self.filter(
                language,
                occurrences=occurrences,
            )

        return record

    def id_name(self, language: str, key: str) -> Optional[dict]:
        """Retrieve a id_name."""
        _ID_NAME_MAP = f"{language}_id_name"
        _VIEWS_ID_MAP = f"{language}_views"
        _OCCURRENCES_ID_MAP = f"{language}_occurrences"

        record_id = self.cache.hget(_ID_NAME_MAP, key)
        if not record_id:
            log.info(f"Key {key} could not be found.")
            raise RuntimeError(
                "missing translation - initialize translation with management command"
            )  # TODO: insert hook to re-initialize translations structure

        record = json.loads(self.cache.get(record_id))

        # NOTE: 1. Compute which views needs refreshing and refresh them and all associations.
        views = [
            view
            for view in record.get("views", [])
            if not self.cache.exists(self.__hash([language, view]))
        ]
        if views and not self.cache.hget(_VIEWS_ID_MAP, record_id):
            _ = self.filter(language, views=views)

        # NOTE: 2. Compute which occurrences needs refreshing and refresh them and all associations.
        occurrences = [
            occurrence
            for occurrence in record.get("occurrences", [])
            if not self.cache.exists(self.__hash([language, occurrence]))
        ]
        if occurrences and not self.cache.hget(_OCCURRENCES_ID_MAP, record_id):
            _ = self.filter(
                language,
                occurrences=occurrences,
            )

        return record

    def _get_all_pages(
        self,
        language: str,
        views: Optional[List[str]] = None,
        occurrences: Optional[List[str]] = None,
        snake_keys: Optional[List[str]] = None,
        page_size: int = 500,
        page: int = 1,
        chain_together: bool = True,
    ) -> Optional[list]:
        """
        This method paginates response and returns list of lists of pages
        """
        url: str = self._filter_url(language)
        params = self.__build_params(views, occurrences, snake_keys, page_size, page)

        response = requests.get(url, params=params, timeout=Client.timeout).json()
        if not response.get("results"):
            return None

        results = [
            response,
        ]
        count = response.get("count")
        next_page = response.get("links", {}).get("next")

        while next_page:
            response = requests.get(next_page, timeout=Client.timeout).json()
            results.append(response)

            page_num = response.get("pages").get("current")
            next_page = response.get("links", {}).get("next")
            log.info(f"Page {page_num} for {language} language.")

        log.info(
            f"There are no more pages. Total count is {count} translations with {params} parameters \n"
            f"for {language} language."
        )

        if chain_together:
            return list(
                chain.from_iterable([result.get("results") for result in results])
            )

        return results

    def filter(
        self,
        language: str,
        views: Optional[List[str]] = None,
        occurrences: Optional[List[str]] = None,
        snake_keys: Optional[List[str]] = None,
        keys_number: int = 500,
        no_cache: bool = False,
        page_size: int = 500,
        page: int = 1,
    ):
        """Filters translations by language, views and occurences."""
        if not language:
            raise django.urls.exceptions.NoReverseMatch("No language selected.")

        if (
            views is None and occurrences is None and snake_keys is None
        ):  # NOTE: If no filtering parameters given, query service directly.
            no_cache = True

        # NOTE: This part potentially still needs auto-pagination for the query
        if no_cache:
            return requests.get(
                self._filter_url(language),
                params=self.__build_params(
                    views, occurrences, snake_keys, page_size, page
                ),
                timeout=Client.timeout,
            )

        if snake_keys and len(snake_keys) > keys_number:
            raise ValidationError(
                f"Number of keys is greater than {keys_number}. Override the keys_number parameter."
            )

        # NOTE: Reverse indexes for lookup of individual keys through `snake_name` or `id_name`.
        # One instance always needs to exists, therefore we never set the TTL on them.
        # However, during the fetching we always check if the `id` exists in grouped indices,
        # which has TTL set to `CACHE_GROUP_KEY_TTL`.
        _SNAKE_NAME_MAP = f"{language}_snake_name"
        _ID_NAME_MAP = f"{language}_id_name"

        # NOTE: Group (and reverse) indexes of views and occurrences for a language.
        _VIEWS_ID_MAP = f"{language}_views"
        _OCCURRENCES_ID_MAP = f"{language}_occurrences"

        def _cache_update(params):
            _cache = {}
            for param in params:
                new_hash = self.__hash(language, param)
                if new_hash in self.cache:
                    _cache.update(self.__load_keys(self.cache.get(new_hash)))

                    # NOTE: Fetched from cache. Remove from fetching list.
                    params.remove(param)

            return _cache

        def _cache_warmup():
            """Closure for prebuilding the result object."""
            _cache = {}

            # 1. Check if any of the specified views is cached.
            if views:
                _cache = _cache_update(views)

            # 2. Check if any of the specified occurrences is cached.
            if occurrences:
                _cache = _cache_update(occurrences)

            # 3. Check if any of the specified snake_keys are cached.
            if snake_keys:
                _cache = _cache_update(snake_keys)

            return _cache

        def _cache_translations(translations: List[dict]):
            """Cache retrieved translations"""
            _cache = {}

            # 4. Compute the caching.
            views, occurrences = defaultdict(list), defaultdict(list)

            for translate in translations:
                _id = translate.get("id")
                if not _id:
                    continue
                _cache[_id] = translate
                _key = translate.get("key")
                _snake = _key.get("snake_name")
                _id_name = _key.get("id_name")
                _views = _key.get("views") or []
                _occurrences = _key.get("occurrences") or []

                data = json.dumps(translate)
                self.cache.set(_id, data)

                # NOTE: Build indexes for search/data access.
                if _snake:
                    self.cache.hset(_SNAKE_NAME_MAP, _snake, _id)

                if _id_name:
                    self.cache.hset(_ID_NAME_MAP, _id_name, _id)

                for view in _views:
                    views[view].append(_id)
                    self.cache.hset(_VIEWS_ID_MAP, _id, view)
                    self.__expire(_VIEWS_ID_MAP)

                for occurrence in _occurrences:
                    occurrences[occurrence].append(_id)
                    self.cache.hset(_OCCURRENCES_ID_MAP, _id, occurrence)
                    self.__expire(_OCCURRENCES_ID_MAP)

            # NOTE: Cache freshly retrieved items.
            for view, keys in views.items():
                self.__set_view(language, view, ids=keys)

            for occurrence, keys in occurrences.items():
                self.__set_occurrence(language, occurrence, ids=keys)

            return _cache

        result = _cache_warmup()

        # 5. Fetch the remaining items.
        translations = self._get_all_pages(
            language, views, occurrences, snake_keys, page_size, page
        )
        if not translations:
            raise RuntimeError(
                "missing translations - initialize translation with management command"
            )

        # 6. Cache new translations and assemble output.
        log.info(f"Caching {len(translations)} translations...")
        result = {**result, **_cache_translations(translations)}
        log.info(
            f"Done. Cached {len(result.items())} items for {len(translations)} translations."
        )
        return result

    def _filter_url(self, language) -> str:
        """Get service filter URL location.

        :returns: url for the `filter` request
        """
        _url = urlparse(f"{self.address}:{self.port}/api/v1/translations/{language}/")
        return _url.geturl()
