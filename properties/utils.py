from django.core.cache import cache
from .models import Property


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