"""
    本地布隆过滤器

    print(BloomFilter.is_repeat(request=RequestGet(url='https://www.baidu.com')))
    print(BloomFilter.is_repeat(request=RequestGet(url='https://www.baidu.com')))
"""
from palp import settings
from palp.network.request import Request
from pybloom_live import ScalableBloomFilter
from palp.filter.filter_base import BaseFilter, FilterLock


class BloomFilter(BaseFilter):
    def __init__(self):
        self.bloom_filter_request = ScalableBloomFilter()
        self.bloom_filter_item = ScalableBloomFilter()

    def is_repeat(self, obj, **kwargs) -> bool:
        """
        获取对应的指纹，通过 本地 的 布隆过滤器 去重

        :param obj:
        :param kwargs:
        :return:
        """
        fingerprint = self.fingerprint(obj=obj)

        if isinstance(obj, Request):
            bloom_filter = self.bloom_filter_request
        else:
            bloom_filter = self.bloom_filter_item

        if settings.STRICT_FILTER:
            with FilterLock():
                return self.judge(fingerprint, bloom_filter)
        else:
            return self.judge(fingerprint, bloom_filter)

    def judge(self, fingerprint, f) -> bool:
        """
        进行判断

        :param fingerprint:
        :param f:
        :return:
        """
        return f.add(fingerprint)
