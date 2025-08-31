from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Property


class PropertyListView(APIView):
    @method_decorator(cache_page(60 * 15))  # 15 minutes
    def get(self, request):
        properties = Property.objects.all()
        return Response([{
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': float(prop.price),
            'location': prop.location,
            'created_at': prop.created_at
        } for prop in properties])