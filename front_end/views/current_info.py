from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404

from accounting.models import CurrentInformation
from front_end.forms import CurrentInformationForm
from front_end.utils.crud import crud, crud_list, crud_delete


def current_info(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/current_info.html', CurrentInformation,
                CurrentInformationForm, pk)


def current_info_list(request):
    return crud_list(request, 'front_end/pages/list/current_info.html', CurrentInformation)


def current_info_delete(request, pk):
    return crud_delete(request, CurrentInformation, pk)
