from core.models import Category
from front_end.forms import CategoryForm
from front_end.utils.crud import crud, crud_list, crud_delete


def category(request, pk=None):
    attr = {'func': 'equal', 'input_key': 'parent', 'error_msg': 'Üst grup kendisi ile aynı olamaz.'}
    return crud(request, 'front_end/pages/create_or_update/category.html', Category, CategoryForm, pk, attr)


def category_list(request):
    return crud_list(request, 'front_end/pages/list/category.html', Category)


def category_delete(request, pk):
    return crud_delete(request, Category, pk)
