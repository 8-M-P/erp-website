from core.models import ProductAttributeValue
from front_end.forms import ProductAttributeValueForm
from front_end.utils.crud import crud, crud_list, crud_delete


def product_attr_value(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/product_attr_value.html', ProductAttributeValue,
                ProductAttributeValueForm, pk)


def product_attr_value_list(request):
    return crud_list(request, 'front_end/pages/list/product_attr_value.html', ProductAttributeValue)


def product_attr_value_delete(request, pk):
    return crud_delete(request, ProductAttributeValue, pk)
