from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, Http404, HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_http_methods

from accounting.models import *
from front_end.forms import CurrentGroupForm
from front_end.utils.crud import crud, crud_list, crud_delete


def success(request):
    return render(request, 'front_end/widgets/result.html')


def old_account_group(request, pk=None):
    template_name = "front_end/pages/create/current_group.html"
    model = CurrentGroup
    form_class = CurrentGroupForm
    data = QueryDict(request.body)
    ajax = True if 'ajax' in data else False
    if pk is not None:
        # Update
        try:
            table = model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise Http404("Does not exist")

        if request.method == "PUT":
            form = form_class(data, instance=table)
            if str(pk) == data['parent']:
                messages.error(request, 'Üst grup kendisi ile aynı olamaz.')
                form.add_error('parent', 'Üst grup kendisi ile aynı olamaz.')
            if form.is_valid():
                form.save()
                messages.success(request, 'Güncelleme başarılı.')
                return render(request, 'front_end/widgets/result.html', {'title': "Güncelleme Başarılı"})
            else:
                messages.warning(request, 'Girilen bilgileri kontol ediniz.')
        else:
            form = form_class(instance=table)
    else:
        if request.method == "POST":
            form = form_class(data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ekleme başarılı.')
                return render(request, 'front_end/widgets/result.html', {'title': "Ekleme Başarılı"})
            else:
                messages.warning(request, 'Girilen bilgileri kontol ediniz.')
        else:
            form = form_class()

    return render(request, template_name, {'form': form, 'ajax': ajax, 'pk': pk})
