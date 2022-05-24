from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from community.models import Community
from product.models import Product
from product.serializer import ProductSerializer, ProductInfoSerializer


@api_view(['POST'])
def create_product(request):
    try:
        product = ProductSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        product.save()
        return Response(request.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)

@api_view(['GET'])
def get_all_products(request):
    products = ProductInfoSerializer(instance=Product.objects.all(), many=True)
    return Response(products.data)

@api_view(['GET'])
def get_product(request, product_id):
    try:
        product = ProductInfoSerializer(instance=Product.objects.get(pk=product_id))
        return Response(product.data)
    except ObjectDoesNotExist:
        return Response({'message': 'No such product'}, status=404)

@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        return Response("deleted")
    except ObjectDoesNotExist:
        return Response({'message': 'No such product'}, status=404)

@api_view(['PUT'])
def update_product(request, product_id):
    try:
        updated_product = ProductSerializer(Product.objects.get(pk=product_id), data=request.data, partial=True)
        updated_product.is_valid(raise_exception=True)
        updated_product.save()
        return Response(updated_product.data)
    except ObjectDoesNotExist:
        return Response({'message': 'No such product'}, status=404)

# def add_product_community(request, product_id):
    # for i in request.data[community]:





