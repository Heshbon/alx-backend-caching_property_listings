from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from .models import Property
from rest_framework.decorators import api_view


@api_view(['GET'])
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all()
    data = [{
        'id': prop.id,
        'title': prop.title,
        'description': prop.description,
        'price': float(prop.price),
        'location': prop.location,
        'created_at': prop.created_at
    } for prop in properties]
    return Response(data)