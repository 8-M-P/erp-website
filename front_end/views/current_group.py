from accounting.models import CurrentGroup
from front_end.forms import CurrentGroupForm
from front_end.utils.crud import crud, crud_list, crud_delete


def current_group(request, pk=None):
    attr = {'func': 'equal', 'input_key': 'parent', 'error_msg': 'Üst grup kendisi ile aynı olamaz.'}
    return crud(request, 'front_end/pages/create_or_update/current_group.html', CurrentGroup, CurrentGroupForm, pk,
                attr)


def current_group_list(request):
    return crud_list(request, 'front_end/pages/list/current_group.html', CurrentGroup)


def current_group_delete(request, pk):
    return crud_delete(request, CurrentGroup, pk)
