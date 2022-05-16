from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


from product.serializer import ProductSerializer


@api_view(['POST'])
def create_product(request):
    product = ProductSerializer(data=request.data)
    product.is_valid(raise_exception=True)
    product.save()
    return Response(request.data)

@api_view([''])
def get_all_products(request):
    pass
