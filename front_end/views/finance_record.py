from accounting.models import FinanceRecord
from front_end.forms import FinanceRecordForm
from front_end.utils.crud import crud, crud_list, crud_delete


def finance_record(request, pk=None):
    return crud(request, 'front_end/pages/create_or_update/finance_record.html', FinanceRecord, FinanceRecordForm, pk)


def finance_record_list(request):
    return crud_list(request, 'front_end/pages/list/finance_record.html', FinanceRecord)


def finance_record_delete(request, pk):
    return crud_delete(request, FinanceRecord, pk)
