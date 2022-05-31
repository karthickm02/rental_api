import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product
from rent.serializer import RentSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def request_rent(request):
    """Requests a renting a product"""

    try:
        logger.debug("Request a rent for product Id {}".format(request.data["product"]))
        request.data["owner"] = Product.objects.get(pk=request.data["product"]).owner.id
        rent = RentSerializer(data=request.data)
        rent.is_valid(raise_exception=True)
        rent.save()
        return Response(rent.data)
    except Product.DoesNotExist:
        logger.debug('No product exists for Id {}'.format(request.data["product"]))
        return Response({'message': 'No such product'}, status=404)

