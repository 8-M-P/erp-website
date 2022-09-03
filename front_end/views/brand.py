from core.models import Brand
from front_end.forms import BrandForm
from front_end.utils.crud import crud, crud_list, crud_delete


def brand(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/brand.html', Brand, BrandForm, pk)


def brand_list(request):
    # print(Brand._meta.get_field('name').verbose_name.title())
    return crud_list(request, 'front_end/pages/list/brand.html', Brand)


def brand_delete(request, pk):
    return crud_delete(request, Brand, pk)
