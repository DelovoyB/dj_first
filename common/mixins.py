from django.core.cache import cache


class CacheMixin:
    def set_get_cache(self, query, cache_name, cache_time):
        """
        Set the cache with the given name to the result of the given query if it doesn't already exist,
        or get the data from the cache if it does exist.

        Args:
            query: The query to get the data from if it doesn't exist in the cache
            cache_name: The name of the cache to set/get
            cache_time: The time in seconds to keep the cache for

        Returns:
            The data from the cache
        """
        data = cache.get(cache_name)

        if not data:
            data = query
            cache.set(cache_name, data, cache_time)

        return data

    def set_get_cache_fn(self, cache_name, query_fn, cache_time):
        """
        Set the cache with the given name to the result of calling the given
        function if it doesn't already exist, or get the data from the cache if
        it does exist.

        Args:
            cache_name: The name of the cache to set/get
            query_fn: The function to call to get the data if it doesn't exist in the cache
            cache_time: The time in seconds to keep the cache for

        Returns:
            The data from the cache
        """
        result = cache.get(cache_name)
        if result is None:
            result = query_fn()
            cache.set(cache_name, result, cache_time)
        return result
