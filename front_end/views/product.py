from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404

from core.models import Product
from front_end.forms import ProductForm
from front_end.utils.crud import crud, crud_list, crud_delete


def product(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/product.html', Product, ProductForm, pk)


def product_list(request):
    return crud_list(request, 'front_end/pages/list/product.html', Product)


def product_list_ajax(request):
    return crud_list(request, 'front_end/pages/ajax/product.html', Product)


def product_delete(request, pk):
    return crud_delete(request, Product, pk)
