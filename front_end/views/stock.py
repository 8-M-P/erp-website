from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404

from core.models import Stock
from front_end.forms import StockForm
from front_end.utils.crud import crud, crud_list, crud_delete


def stock(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/stock.html', Stock, StockForm, pk)


def stock_list(request):
    return crud_list(request, 'front_end/pages/list/stock.html', Stock)


def stock_delete(request, pk):
    return crud_delete(request, Stock, pk)
