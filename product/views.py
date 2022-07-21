import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product
from product.serializer import ProductSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def create_product(request):
    try:
        logger.debug('Create product API called. \nData: {}'.format(request.data))
        request.data['owner'] = request.user.id
        product = ProductSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        product.save()
        return Response(product.data)
    except ValidationError as error:
        logger.debug('validation Error, Invalid inputs')
        return Response({'message': error.message}, status=400)


@api_view(['GET'])
@protected_resource(scopes=['admin'])
def get_all_products(request):
    logger.debug('List products method called.')
    products = ProductSerializer(instance=Product.objects.all(), many=True,
                                 fields=('id', 'name', 'owner', 'rate', 'description',
                                         'is_available', 'rent_end_date', 'picture'))
    return Response(products.data)


@api_view(['GET'])
def get_product(request, product_id):
    try:
        logger.debug('Get product API called for Id {}'.format(product_id))
        product = ProductSerializer(instance=Product.objects.get(pk=product_id),
                                    fields=('id', 'name', 'owner', 'rate', 'description',
                                            'is_available', 'rent_end_date', 'picture'))
        return Response(product.data)
    except ObjectDoesNotExist:
        logger.debug('No product exists for Id {}'.format(product_id))
        return Response({'message': 'No such product'}, status=404)


@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        logger.debug('Delete community API called for Id {}'.format(product_id))
        product = Product.objects.get(pk=product_id)
        product.delete()
        return Response({'message': 'Product Deleted'})
    except ObjectDoesNotExist:
        logger.debug('No product exists for Id {}'.format(product_id))
        return Response({'message': 'No such product'}, status=404)


@api_view(['PUT'])
def update_product(request, product_id):
    try:
        logger.debug('Update product API called for Id {}'.format(product_id))
        product = Product.objects.get(pk=product_id)
        if product.owner == request.user:
            updated_product = ProductSerializer(product,
                                                data=request.data, partial=True)
            updated_product.is_valid(raise_exception=True)
            updated_product.save()
            return Response(ProductSerializer(instance=product,
                                              fields=('id', 'name', 'owner', 'rate', 'description',
                                                      'is_available', 'rent_end_date', 'picture')).data)
        else:
            return Response({'message': "You can't make changes"})
    except ObjectDoesNotExist:
        logger.debug('No product exists for Id {}'.format(product_id))
        return Response({'message': 'No such product'}, status=404)
