from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, QueryDict, HttpResponse
from django.shortcuts import render, redirect


def crud(request, template, model, form_class, pk=None, attr=None, return_bool=False):
    """
    Create, Update and Delete Function
     Allow Methods: ['GET', 'PUT', 'POST', 'DELETE']
    :param return_bool: If True return Boolen result instead of template
    :param attr:
    :param request:
    :param template: Template file path exp: "app_name/template_name.html"
    :param model: Modelname
    :param form_class:  FormName
    :param pk: Not Requred
    :return:
    """
    if request.method == "POST":
        post = request.POST
    else:
        post = False
    data = QueryDict(request.body)
    if pk is not None:
        # Update
        try:
            table = model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise Http404("Does not exist")
        if request.method == "POST":
            form = form_class(data, instance=table)
            if attr is not None:
                if attr['func'] == 'equal':
                    if str(pk) == data[attr['input_key']]:
                        messages.error(request, attr['error_msg'])
                        form.add_error(attr['input_key'], attr['error_msg'])
                if attr['func'] == 'notequal':
                    if str(pk) != data[attr['input_key']]:
                        messages.error(request, attr['error_msg'])
                        form.add_error(attr['input_key'], attr['error_msg'])
            if form.is_valid():
                form.save()
                messages.success(request, 'Güncelleme başarılı.')
                if return_bool:
                    return True
                return redirect('result')
            else:
                messages.warning(request, 'Girilen bilgileri kontol ediniz.')
                form = form_class(data or None, instance=table or None)

        elif request.method == "DELETE":
            if table.delete():
                messages.success(request, 'Silme başarılı.')
                return redirect('result')
            else:
                messages.success(request, 'Silme işlemi gerçekleşmedi.')
                return redirect('result')
        else:
            form = form_class(instance=table)
    else:
        form = form_class(data=data or None, initial=data.dict() or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Ekleme başarılı.')
                if return_bool:
                    return True
                return redirect('result')
            else:
                messages.warning(request, 'Girilen bilgileri kontol ediniz.')

    return render(request, template, {'form': form, 'pk': pk})


def crud_delete(request, model, pk):
    if pk is not None:
        try:
            table = model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise Http404("Does not exist")
        if table.delete():
            messages.success(request, 'Silme başarılı.')
            return redirect('result')
        else:
            messages.success(request, 'Silme işlemi gerçekleşmedi.')
            return redirect('result')
    else:
        raise Http404("Does not exist")


def crud_list(request, template, model, content=None):
    table = model.objects.all()
    if table.exists() is False:
        table = None
    return render(request, template, {'table': table, 'content': content})
