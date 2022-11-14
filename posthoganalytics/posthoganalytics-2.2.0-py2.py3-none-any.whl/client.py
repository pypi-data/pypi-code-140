import atexit
import logging
import numbers
from datetime import datetime, timedelta
from uuid import UUID

from dateutil.tz import tzutc
from six import string_types

from posthoganalytics.consumer import Consumer
from posthoganalytics.feature_flags import InconclusiveMatchError, match_feature_flag_properties
from posthoganalytics.poller import Poller
from posthoganalytics.request import APIError, batch_post, decide, get
from posthoganalytics.utils import SizeLimitedDict, clean, guess_timezone
from posthoganalytics.version import VERSION

try:
    import queue
except ImportError:
    import Queue as queue


ID_TYPES = (numbers.Number, string_types, UUID)
MAX_DICT_SIZE = 50_000


class Client(object):
    """Create a new PostHog client."""

    log = logging.getLogger("posthog")

    def __init__(
        self,
        api_key=None,
        host=None,
        debug=False,
        max_queue_size=10000,
        send=True,
        on_error=None,
        flush_at=100,
        flush_interval=0.5,
        gzip=False,
        max_retries=3,
        sync_mode=False,
        timeout=15,
        thread=1,
        poll_interval=30,
        personal_api_key=None,
        project_api_key=None,
    ):

        self.queue = queue.Queue(max_queue_size)

        # api_key: This should be the Team API Key (token), public
        self.api_key = project_api_key or api_key

        require("api_key", self.api_key, string_types)

        self.on_error = on_error
        self.debug = debug
        self.send = send
        self.sync_mode = sync_mode
        self.host = host
        self.gzip = gzip
        self.timeout = timeout
        self.feature_flags = None
        self.group_type_mapping = None
        self.poll_interval = poll_interval
        self.poller = None
        self.distinct_ids_feature_flags_reported = SizeLimitedDict(MAX_DICT_SIZE, set)

        # personal_api_key: This should be a generated Personal API Key, private
        self.personal_api_key = personal_api_key
        if debug:
            # Ensures that debug level messages are logged when debug mode is on.
            # Otherwise, defaults to WARNING level. See https://docs.python.org/3/howto/logging.html#what-happens-if-no-configuration-is-provided
            logging.basicConfig()
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.WARNING)

        if sync_mode:
            self.consumers = None
        else:
            # On program exit, allow the consumer thread to exit cleanly.
            # This prevents exceptions and a messy shutdown when the
            # interpreter is destroyed before the daemon thread finishes
            # execution. However, it is *not* the same as flushing the queue!
            # To guarantee all messages have been delivered, you'll still need
            # to call flush().
            if send:
                atexit.register(self.join)
            for n in range(thread):
                self.consumers = []
                consumer = Consumer(
                    self.queue,
                    self.api_key,
                    host=host,
                    on_error=on_error,
                    flush_at=flush_at,
                    flush_interval=flush_interval,
                    gzip=gzip,
                    retries=max_retries,
                    timeout=timeout,
                )
                self.consumers.append(consumer)

                # if we've disabled sending, just don't start the consumer
                if send:
                    consumer.start()

    def identify(self, distinct_id=None, properties=None, context=None, timestamp=None, uuid=None):
        properties = properties or {}
        context = context or {}
        require("distinct_id", distinct_id, ID_TYPES)
        require("properties", properties, dict)

        msg = {
            "timestamp": timestamp,
            "context": context,
            "distinct_id": distinct_id,
            "$set": properties,
            "event": "$identify",
            "uuid": uuid,
        }

        return self._enqueue(msg)

    def get_feature_variants(self, distinct_id, groups=None, person_properties=None, group_properties=None):
        require("distinct_id", distinct_id, ID_TYPES)

        if groups:
            require("groups", groups, dict)
        else:
            groups = {}

        request_data = {
            "distinct_id": distinct_id,
            "groups": groups,
            "person_properties": person_properties,
            "group_properties": group_properties,
        }
        resp_data = decide(self.api_key, self.host, timeout=10, **request_data)
        return resp_data["featureFlags"]

    def capture(
        self,
        distinct_id=None,
        event=None,
        properties=None,
        context=None,
        timestamp=None,
        uuid=None,
        groups=None,
        send_feature_flags=False,
    ):
        properties = properties or {}
        context = context or {}
        require("distinct_id", distinct_id, ID_TYPES)
        require("properties", properties, dict)
        require("event", event, string_types)

        msg = {
            "properties": properties,
            "timestamp": timestamp,
            "context": context,
            "distinct_id": distinct_id,
            "event": event,
            "uuid": uuid,
        }

        if groups:
            require("groups", groups, dict)
            msg["properties"]["$groups"] = groups

        if send_feature_flags:
            try:
                feature_variants = self.get_feature_variants(distinct_id, groups)
            except Exception as e:
                self.log.exception(f"[FEATURE FLAGS] Unable to get feature variants: {e}")
            else:
                for feature, variant in feature_variants.items():
                    msg["properties"]["$feature/{}".format(feature)] = variant
                msg["properties"]["$active_feature_flags"] = list(feature_variants.keys())

        return self._enqueue(msg)

    def set(self, distinct_id=None, properties=None, context=None, timestamp=None, uuid=None):
        properties = properties or {}
        context = context or {}
        require("distinct_id", distinct_id, ID_TYPES)
        require("properties", properties, dict)

        msg = {
            "timestamp": timestamp,
            "context": context,
            "distinct_id": distinct_id,
            "$set": properties,
            "event": "$set",
            "uuid": uuid,
        }

        return self._enqueue(msg)

    def set_once(self, distinct_id=None, properties=None, context=None, timestamp=None, uuid=None):
        properties = properties or {}
        context = context or {}
        require("distinct_id", distinct_id, ID_TYPES)
        require("properties", properties, dict)

        msg = {
            "timestamp": timestamp,
            "context": context,
            "distinct_id": distinct_id,
            "$set_once": properties,
            "event": "$set_once",
            "uuid": uuid,
        }

        return self._enqueue(msg)

    def group_identify(self, group_type=None, group_key=None, properties=None, context=None, timestamp=None, uuid=None):
        properties = properties or {}
        context = context or {}
        require("group_type", group_type, ID_TYPES)
        require("group_key", group_key, ID_TYPES)
        require("properties", properties, dict)

        msg = {
            "event": "$groupidentify",
            "properties": {
                "$group_type": group_type,
                "$group_key": group_key,
                "$group_set": properties,
            },
            "distinct_id": "${}_{}".format(group_type, group_key),
            "timestamp": timestamp,
            "context": context,
            "uuid": uuid,
        }

        return self._enqueue(msg)

    def alias(self, previous_id=None, distinct_id=None, context=None, timestamp=None, uuid=None):
        context = context or {}

        require("previous_id", previous_id, ID_TYPES)
        require("distinct_id", distinct_id, ID_TYPES)

        msg = {
            "properties": {
                "distinct_id": previous_id,
                "alias": distinct_id,
            },
            "timestamp": timestamp,
            "context": context,
            "event": "$create_alias",
            "distinct_id": previous_id,
        }

        return self._enqueue(msg)

    def page(self, distinct_id=None, url=None, properties=None, context=None, timestamp=None, uuid=None):
        properties = properties or {}
        context = context or {}

        require("distinct_id", distinct_id, ID_TYPES)
        require("properties", properties, dict)

        require("url", url, string_types)
        properties["$current_url"] = url

        msg = {
            "event": "$pageview",
            "properties": properties,
            "timestamp": timestamp,
            "context": context,
            "distinct_id": distinct_id,
            "uuid": uuid,
        }

        return self._enqueue(msg)

    def _enqueue(self, msg):
        """Push a new `msg` onto the queue, return `(success, msg)`"""
        timestamp = msg["timestamp"]
        if timestamp is None:
            timestamp = datetime.utcnow().replace(tzinfo=tzutc())

        require("timestamp", timestamp, datetime)
        require("context", msg["context"], dict)

        # add common
        timestamp = guess_timezone(timestamp)
        msg["timestamp"] = timestamp.isoformat()

        # only send if "uuid" is truthy
        if "uuid" in msg:
            uuid = msg.pop("uuid")
            if uuid:
                msg["uuid"] = stringify_id(uuid)

        if not msg.get("properties"):
            msg["properties"] = {}
        msg["properties"]["$lib"] = "posthog-python"
        msg["properties"]["$lib_version"] = VERSION

        msg["distinct_id"] = stringify_id(msg.get("distinct_id", None))

        msg = clean(msg)
        self.log.debug("queueing: %s", msg)

        # if send is False, return msg as if it was successfully queued
        if not self.send:
            return True, msg

        if self.sync_mode:
            self.log.debug("enqueued with blocking %s.", msg["event"])
            batch_post(self.api_key, self.host, gzip=self.gzip, timeout=self.timeout, batch=[msg])

            return True, msg

        try:
            self.queue.put(msg, block=False)
            self.log.debug("enqueued %s.", msg["event"])
            return True, msg
        except queue.Full:
            self.log.warning("analytics-python queue is full")
            return False, msg

    def flush(self):
        """Forces a flush from the internal queue to the server"""
        queue = self.queue
        size = queue.qsize()
        queue.join()
        # Note that this message may not be precise, because of threading.
        self.log.debug("successfully flushed about %s items.", size)

    def join(self):
        """Ends the consumer thread once the queue is empty.
        Blocks execution until finished
        """
        for consumer in self.consumers:
            consumer.pause()
            try:
                consumer.join()
            except RuntimeError:
                # consumer thread has not started
                pass

        if self.poller:
            self.poller.stop()

    def shutdown(self):
        """Flush all messages and cleanly shutdown the client"""
        self.flush()
        self.join()

    def _load_feature_flags(self):
        try:
            response = get(
                self.personal_api_key, f"/api/feature_flag/local_evaluation/?token={self.api_key}", self.host
            )
            self.feature_flags = response["flags"] or []
            self.group_type_mapping = response["group_type_mapping"] or {}

        except APIError as e:
            if e.status == 401:
                raise APIError(
                    status=401,
                    message="You are using a write-only key with feature flags. "
                    "To use feature flags, please set a personal_api_key "
                    "More information: https://posthog.com/docs/api/overview",
                )
            else:
                self.log.error(f"[FEATURE FLAGS] Error loading feature flags: {e}")
        except Exception as e:
            self.log.warning(
                "[FEATURE FLAGS] Fetching feature flags failed with following error. We will retry in %s seconds."
                % self.poll_interval
            )
            self.log.warning(e)

        self._last_feature_flag_poll = datetime.utcnow().replace(tzinfo=tzutc())

    def load_feature_flags(self):
        if not self.personal_api_key:
            self.log.warning("[FEATURE FLAGS] You have to specify a personal_api_key to use feature flags.")
            self.feature_flags = []
            return

        self._load_feature_flags()
        if not (self.poller and self.poller.is_alive()):
            self.poller = Poller(interval=timedelta(seconds=self.poll_interval), execute=self._load_feature_flags)
            self.poller.start()

    def _compute_flag_locally(self, feature_flag, distinct_id, *, groups={}, person_properties={}, group_properties={}):

        if feature_flag.get("ensure_experience_continuity", False):
            raise InconclusiveMatchError("Flag has experience continuity enabled")

        if not feature_flag.get("active"):
            return False

        flag_filters = feature_flag.get("filters") or {}
        aggregation_group_type_index = flag_filters.get("aggregation_group_type_index")
        if aggregation_group_type_index is not None:
            group_name = self.group_type_mapping.get(str(aggregation_group_type_index))

            if not group_name:
                self.log.warning(
                    f"[FEATURE FLAGS] Unknown group type index {aggregation_group_type_index} for feature flag {feature_flag['key']}"
                )
                # failover to `/decide/`
                raise InconclusiveMatchError("Flag has unknown group type index")

            if group_name not in groups:
                # Group flags are never enabled in `groups` aren't passed in
                # don't failover to `/decide/`, since response will be the same
                self.log.warning(
                    f"[FEATURE FLAGS] Can't compute group feature flag: {feature_flag['key']} without group names passed in"
                )
                return False

            focused_group_properties = group_properties[group_name]
            return match_feature_flag_properties(feature_flag, groups[group_name], focused_group_properties)
        else:
            return match_feature_flag_properties(feature_flag, distinct_id, person_properties)

    def feature_enabled(
        self,
        key,
        distinct_id,
        *,
        groups={},
        person_properties={},
        group_properties={},
        only_evaluate_locally=False,
        send_feature_flag_events=True,
    ):
        response = self.get_feature_flag(
            key,
            distinct_id,
            groups=groups,
            person_properties=person_properties,
            group_properties=group_properties,
            only_evaluate_locally=only_evaluate_locally,
            send_feature_flag_events=send_feature_flag_events,
        )

        if response is None:
            return None
        return bool(response)

    def get_feature_flag(
        self,
        key,
        distinct_id,
        *,
        groups={},
        person_properties={},
        group_properties={},
        only_evaluate_locally=False,
        send_feature_flag_events=True,
    ):
        require("key", key, string_types)
        require("distinct_id", distinct_id, ID_TYPES)
        require("groups", groups, dict)

        if self.feature_flags == None and self.personal_api_key:
            self.load_feature_flags()
        response = None

        # If loading in previous line failed
        if self.feature_flags:
            for flag in self.feature_flags:
                if flag["key"] == key:
                    try:
                        response = self._compute_flag_locally(
                            flag,
                            distinct_id,
                            groups=groups,
                            person_properties=person_properties,
                            group_properties=group_properties,
                        )
                        self.log.debug(f"Successfully computed flag locally: {key} -> {response}")
                    except InconclusiveMatchError as e:
                        self.log.debug(f"Failed to compute flag {key} locally: {e}")
                        continue
                    except Exception as e:
                        self.log.exception(f"[FEATURE FLAGS] Error while computing variant locally: {e}")
                        continue

        flag_was_locally_evaluated = response is not None
        if not flag_was_locally_evaluated and not only_evaluate_locally:
            try:
                feature_flags = self.get_feature_variants(
                    distinct_id, groups=groups, person_properties=person_properties, group_properties=group_properties
                )
                response = feature_flags.get(key)
                if response is None:
                    response = False
                self.log.debug(f"Successfully computed flag remotely: #{key} -> #{response}")
            except Exception as e:
                self.log.exception(f"[FEATURE FLAGS] Unable to get flag remotely: {e}")

        feature_flag_reported_key = f"{key}_{str(response)}"
        if (
            feature_flag_reported_key not in self.distinct_ids_feature_flags_reported[distinct_id]
            and send_feature_flag_events
        ):
            self.capture(
                distinct_id,
                "$feature_flag_called",
                {
                    "$feature_flag": key,
                    "$feature_flag_response": response,
                    "locally_evaluated": flag_was_locally_evaluated,
                },
                groups=groups,
            )
            self.distinct_ids_feature_flags_reported[distinct_id].add(feature_flag_reported_key)
        return response

    def get_all_flags(
        self, distinct_id, *, groups={}, person_properties={}, group_properties={}, only_evaluate_locally=False
    ):
        require("distinct_id", distinct_id, ID_TYPES)
        require("groups", groups, dict)

        if self.feature_flags == None and self.personal_api_key:
            self.load_feature_flags()

        response = {}
        fallback_to_decide = False

        # If loading in previous line failed
        if self.feature_flags:
            for flag in self.feature_flags:
                try:
                    response[flag["key"]] = self._compute_flag_locally(
                        flag,
                        distinct_id,
                        groups=groups,
                        person_properties=person_properties,
                        group_properties=group_properties,
                    )
                except InconclusiveMatchError as e:
                    # No need to log this, since it's just telling us to fall back to `/decide`
                    fallback_to_decide = True
                except Exception as e:
                    self.log.exception(f"[FEATURE FLAGS] Error while computing variant: {e}")
                    fallback_to_decide = True
        else:
            fallback_to_decide = True

        if fallback_to_decide and not only_evaluate_locally:
            try:
                feature_flags = self.get_feature_variants(
                    distinct_id, groups=groups, person_properties=person_properties, group_properties=group_properties
                )
                response = {**response, **feature_flags}
            except Exception as e:
                self.log.exception(f"[FEATURE FLAGS] Unable to get feature variants: {e}")

        return response


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = "{0} must have {1}, got: {2}".format(name, data_type, field)
        raise AssertionError(msg)


def stringify_id(val):
    if val is None:
        return None
    if isinstance(val, string_types):
        return val
    return str(val)
