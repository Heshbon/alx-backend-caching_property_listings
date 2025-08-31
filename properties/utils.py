from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property


# Logging set up
logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Fetch all properties using low-level caching.
    Cache duration: 1 hour (3600 seconds)
    """
    properties = cache.get('all_properties')

    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, 3600)

    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache metrics.
    Returns a dictionary containing hits, misses, and hit ratio.
    """
    try:
        redis_conn = get_redis_connection()

        # Get cache metrics from Redis INFO command
        info = redis_conn.info()

        # Extract metrics
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)

        # Calculate hit ratio
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        # Log metrics
        logger.info(
            f"Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2%}")

        # Return metrics dictionary
        return {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio,
            'total_requests': total_requests
        }

    except Exception as e:
        logger.error(f"Error getting cache metrics: {str(e)}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0.0,
            'total_requests': 0
        }