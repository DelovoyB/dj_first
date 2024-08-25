from django.core.cache import cache


class CacheMixin:
    def set_get_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)

        if not data:
            data = query
            cache.set(cache_name, data, cache_time)

        return data

    def set_get_cache_fn(self, cache_name, query_fn, cache_time):
        result = cache.get(cache_name)
        if result is None:
            result = query_fn()
            cache.set(cache_name, result, cache_time)
        return result