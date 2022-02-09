import sys
from io import BytesIO
import requests
from PIL import Image
from  map_function import get_response, get_ll, get_spn, get_object, show_map


toponym_to_find = " ".join(sys.argv[1:])
# Получаем первый топоним из ответа геокодера.
toponym = get_response(toponym_to_find)
# Координаты центра топонима:

# Собираем параметры для запроса к StaticMapsAPI:
param_ll = get_ll(toponym)
param_spn = get_spn(toponym)


response = get_object(param_ll, param_spn)
show_map(response)
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы