"""
    redis 队列
    使用了 pickle 并使用 zlib 压缩
"""
import zlib
import pickle
from palp import settings
from palp.sequence.sequence_base import BaseSequence


# 先进先出队列
class FIFOSequence(BaseSequence):
    def put(self, obj, timeout: int = None):
        """
        添加任务

        :param obj:
        :param timeout:
        :return:
        """
        from palp.conn import redis_conn

        redis_conn.rpush(settings.REDIS_KEY_QUEUE_REQUEST, zlib.compress(pickle.dumps(obj)))

    def get(self, timeout: int = None):
        """
        获取任务（这里是返回的对象）

        :return:
        """
        from palp.conn import redis_conn

        result = redis_conn.blpop(settings.REDIS_KEY_QUEUE_REQUEST, timeout=timeout)
        if result:
            return pickle.loads(zlib.decompress(result[-1]))  # 这里不需要 decode 因为是对象

    def empty(self):
        """
        判断队列是否为空

        :return:
        """
        from palp.conn import redis_conn

        return redis_conn.llen(settings.REDIS_KEY_QUEUE_REQUEST) == 0


# 后进先出队列
class LIFOSequence(FIFOSequence):
    def get(self, timeout: int = None):
        """
        获取任务
        :return:
        """
        from palp.conn import redis_conn

        result = redis_conn.brpop(settings.REDIS_KEY_QUEUE_REQUEST, timeout=timeout)
        if result:
            return pickle.loads(zlib.decompress(result[-1]))


# 优先级队列
class PrioritySequence(BaseSequence):
    def put(self, obj, timeout: int = None):
        """
        添加任务

        :param obj:
        :param timeout:
        :return:
        """
        from palp.conn import redis_conn

        if hasattr(obj, 'level'):
            level = obj.level
        else:
            level = 100

        redis_conn.zadd(settings.REDIS_KEY_QUEUE_REQUEST, {zlib.compress(pickle.dumps(obj)): level})

    def get(self, timeout: int = None):
        """
        获取任务（这里是返回的对象）

        :return:
        """
        from palp.conn import redis_conn

        result = redis_conn.bzpopmin(settings.REDIS_KEY_QUEUE_REQUEST, timeout=timeout)
        if result:
            return pickle.loads(zlib.decompress(result[1]))

    def empty(self):
        """
        判断队列是否为空

        :return:
        """
        from palp.conn import redis_conn

        return redis_conn.zcard(settings.REDIS_KEY_QUEUE_REQUEST) == 0
