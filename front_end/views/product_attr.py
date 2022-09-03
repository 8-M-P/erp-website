from core.models import ProductAttribute
from front_end.forms import ProductAttributeForm
from front_end.utils.crud import crud, crud_list, crud_delete


def product_attr(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/product_attr.html', ProductAttribute, ProductAttributeForm,
                pk)


def product_attr_list(request):
    return crud_list(request, 'front_end/pages/list/product_attr.html', ProductAttribute)


def product_attr_delete(request, pk):
    return crud_delete(request, ProductAttribute, pk)
