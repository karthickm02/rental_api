import logging

import cv2
import pytesseract
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product
from rent.models import Rent
from rent.serializer import RentSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def request_rent(request):
    """Requests a renting a product"""

    try:
        logger.debug("Request a rent for product Id {}".format(request.data["product"]))
        request.data["owner"] = Product.objects.get(pk=request.data["product"]).owner.id
        request.data['card_number'] = get_id_number(request.data['card_image'])
        request.data['user'] = request.user.id
        rent = RentSerializer(data=request.data)
        rent.is_valid(raise_exception=True)
        rent.save()
        return Response(rent.data)
    except Product.DoesNotExist:
        logger.debug('No product exists for Id {}'.format(request.data["product"]))
        return Response({'message': 'No such product'}, status=404)


def get_id_number(file_name):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    img = cv2.imread(filename=f"C:\\Users\Lenovo\\Documents\\idcards\\{file_name}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (1272, 712))

    data = pytesseract.image_to_data(img, config=r'--oem 3 --psm 6 outputbase digits')
    for x, d in enumerate(data.splitlines()):
        if x != 0:
            d = d.split()
            if len(d) == 12:
                if len(str(d[11])) == 12:
                    return d[11]

@api_view(['GET'])
@protected_resource(scopes=['admin'])
def get_all_rents(request):
    logger.debug('List products method called.')
    rents = RentSerializer(instance=Rent.objects.all(), many=True)
    return Response(rents.data)
