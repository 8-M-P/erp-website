from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404

from accounting.models import CurrentBankInformation
from front_end.forms import CurrentBankInformationForm
from front_end.utils.crud import crud, crud_list, crud_delete


def current_bank_info(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/current_bank_info.html', CurrentBankInformation,
                CurrentBankInformationForm, pk)


def current_bank_info_list(request):
    return crud_list(request, 'front_end/pages/list/current_bank_info.html', CurrentBankInformation)


def current_bank_info_delete(request, pk):
    return crud_delete(request, CurrentBankInformation, pk)
