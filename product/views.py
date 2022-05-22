from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product
from product.serializer import ProductSerializer

@api_view(['POST'])
def create_product(request):
    # request.data["community"] make validation for user should present in the lis of communities
    product = ProductSerializer(data=request.data)
    product.is_valid(raise_exception=True)
    product.save()
    return Response(request.data)

@api_view(['GET'])
def get_all_products(request):
    products = ProductSerializer(instance=Product.objects.all(), many=True)
    return Response(products.data)

@api_view(['GET'])
def get_product(request, product_id):
    product = ProductSerializer(instance=Product.objects.get(pk=product_id))
    return Response(product.data)

@api_view(['DELETE'])
def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return Response("deleted")

@api_view(['PUT'])
def update_product(request, product_id):
    updated_product = ProductSerializer(Product.objects.get(pk=product_id), data=request.data, partial=True)
    updated_product.is_valid(raise_exception=True)
    updated_product.save()
    return Response("updated")


