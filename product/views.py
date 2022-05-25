import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product
from product.serializer import ProductSerializer, ProductInfoSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def create_product(request):
    try:
        logger.debug('Create product API called. \nData: {}'.format(request.data))
        product = ProductSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        product.save()
        return Response(product.data)
    except ValidationError as error:
        logger.debug('validation Error, Invalid inputs')
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
def get_all_products(request):
    logger.debug('List products method called.')
    products = ProductInfoSerializer(instance=Product.objects.all(), many=True)
    return Response(products.data)


@api_view(['GET'])
def get_product(request, product_id):
    try:
        logger.debug('Get product API called for Id {}'.format(product_id))
        product = ProductInfoSerializer(instance=Product.objects.get(pk=product_id))
        return Response(product.data)
    except ObjectDoesNotExist:
        logger.debug('No product exists for Id {}'.format(product_id))
        return Response({'message': 'No such product'}, status=404)


@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        logger.debug('Delete community API called for Id {}'.format(community_id))
        product = Product.objects.get(pk=product_id)
        product.delete()
        return Response("deleted")
    except ObjectDoesNotExist:
        logger.debug('No product exists for Id {}'.format(product_id))
        return Response({'message': 'No such product'}, status=404)


@api_view(['PUT'])
def update_product(request, product_id):
    try:
        logger.debug('Update product API called for Id {}'.format(product_id))
        updated_product = ProductSerializer(Product.objects.get(pk=product_id),
                                            data=request.data, partial=True)
        updated_product.is_valid(raise_exception=True)
        updated_product.save()
        return Response(updated_product.data)
    except ObjectDoesNotExist:
        logger.debug('No product exists for Id {}'.format(product_id))
        return Response({'message': 'No such product'}, status=404)


