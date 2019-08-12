from olive.exc import CacheNotFound
from pprint import pformat
import ujson


class CacheWrapper(object):
    def __init__(self, app, key_pattern):
        self.app = app
        self.key_pattern = key_pattern

    def get_cache(self, key):
        final_key = self.key_pattern.format(str(key))
        self.app.log.debug('reading {} from cache...'.format(final_key))
        data = self.app.cache.get(final_key)
        if data is None:
            self.app.log.info('cache {} not found!'.format(final_key))
            raise CacheNotFound

        data = ujson.loads(data)
        self.app.log.info('cache {} data: {}'.format(final_key, pformat(data)))
        return data

    def write_cache(self, key, value):
        final_key = self.key_pattern.format(str(key))
        self.app.log.debug('writing cache to {}'.format(final_key))
        self.app.cache.set(key=final_key, value=ujson.dumps(value))
        self.app.log.info('cache {} saved ;)'.format(final_key))

    def delete(self, key):
        final_key = self.key_pattern.format(str(key))
        self.app.log.debug('deleting {} cache...'.format(final_key))
        self.app.cache.delete(final_key)
        self.app.log.info('deleted {} cache'.format(final_key))

    def delete_by_pattern(self, pattern):
        self.app.log.debug('deleting cache with the pattern: {}'.format(pattern))
        self.app.cache.delete_by_pattern(pattern)
        self.app.log.info('{} cache pattern keys are purged'.format(pattern))
