from accounting.models import FinanceRecord, FinanceRecordContent, CurrentInformation
from core.models import Product
from front_end.forms import FinanceRecordForm
from front_end.utils.crud import crud, crud_list, crud_delete

import json
from datetime import datetime
from django.contrib import messages
from django.http import Http404, HttpResponseBadRequest, QueryDict, HttpResponse, JsonResponse
from django.shortcuts import render, redirect


def bill_calc(products=None):
    """
    products = [
        {'pk': 2, 'tax_rate': 10, 'discount_rate': 15, 'quantity': 1, 'unit_price': 1000.00},
        {'pk': 3, 'tax_rate': 18, 'discount_rate': 5, 'quantity': 2, 'unit_price': 5300.00},
    ]

    total = price * unit
    discount_sum = total * discount / 100
    sub_total = total * (100 - discount) / 100
    final_total = sub_total * (1 + (tax_rate / 100))
    vat_total = (final_total - (final_total / (1 + tax_rate / 100))))
    """
    products = json.loads(products)
    product_bills = []

    def product_bill_calc(product):
        total = product.get('unit_price') * product.get('quantity')
        discount_sum = total * product.get('discount_rate') / 100
        sub_total = total * (100 - product.get('discount_rate')) / 100
        final_total = sub_total * (1 + (product.get('tax_rate') / 100))
        vat_total = final_total - (final_total / (1 + product.get('tax_rate') / 100))
        product_bill = {
            'hidden': {
                'pk': product.get('pk'),
                'discount_sum': round(discount_sum, 2),
                'sub_total': round(sub_total, 2),
                'vat_total': round(vat_total, 2),
                'total': round(total, 2),
            },
            'public': {
                'sku': product.get('sku'),
                'name': product.get('name'),
                'measurement_unit': product.get('measurement_unit'),
                'tax_rate': product.get('tax_rate'),
                'discount_rate': product.get('discount_rate'),
                'quantity': product.get('quantity'),
                'unit_price': product.get('unit_price'),
                'final_total': round(final_total, 2),
            }
        }
        product_bills.append(product_bill)

    if isinstance(products, dict):
        product = products.copy()
        product_bill_calc(product)
    elif isinstance(products, list):
        for product in products:
            product_bill_calc(product)

    bill_result = {
        'total': 0.0,
        'discount_sum': 0.0,
        'sub_total': 0.0,
        'vat_total': 0.0,
        'final_total': 0.0,
    }
    for bill in product_bills:
        bill_result = {
            'total': round(bill_result.get('total') + round(bill.get('hidden').get('total'), 2), 2),
            'discount_sum': round(bill_result.get('discount_sum') + round(bill.get('hidden').get('discount_sum'), 2),
                                  2),
            'sub_total': round(bill_result.get('sub_total') + round(bill.get('hidden').get('sub_total'), 2), 2),
            'vat_total': round(bill_result.get('vat_total') + round(bill.get('hidden').get('vat_total'), 2), 2),
            'final_total': round(bill_result.get('final_total') + round(bill.get('public').get('final_total'), 2), 2),
        }
    print({'bill_result': bill_result, 'products_bills': product_bills})
    return JsonResponse({'bill_result': bill_result, 'products_bills': product_bills})


def bill_update(request):
    if request.method == "POST":
        data = request.body
        return bill_calc(data)
    return HttpResponseBadRequest()


def finance_record(request, pk=None):
    record_content = []
    model = FinanceRecord
    form_class = FinanceRecordForm
    template = "front_end/pages/create_or_update/finance_record.html"
    # TODO: Content add to the record
    # TODO: Validation for max and min value, and negative value and empty value, and zero value and read-only currency inputs
    # TODO: Make system for stock management and money management
    if request.method == "POST":
        # Before save the record, we need to prepare the content of the record
        post = request.POST.copy()
        # create for loop for each records in post
        record_content = []
        for record in post.getlist('records'):
            record = json.loads(record)
            hidden = record.get('hidden')
            public = record.get('public')
            record_content.append(FinanceRecordContent(finance_id=pk,
                                                       product_id=hidden.get('pk'),
                                                       discount_rate=public.get('discount_rate'),
                                                       quantity=public.get('quantity'),
                                                       unit_price=public.get('unit_price'),
                                                       total=hidden.get('total'),
                                                       discount_sum=hidden.get('discount_sum'),
                                                       sub_total=hidden.get('sub_total'),
                                                       vat_total=hidden.get('vat_total'),
                                                       final_total=public.get('final_total'), ))

        # convert date to Postgres format
        def date_convert(p, fields):
            for field in fields:
                p[field] = datetime.strptime(p[field], '%m/%d/%Y').strftime('%Y-%m-%d')

        # convert currency to float
        def currency_convert(p, names):
            for name in names:
                if p[name] == "":
                    p[name] = "0.0"

                if "," in p[name]:
                    p[name] = float(p[name].replace(',', ''))
                else:
                    p[name] = float(p[name])

        currency_convert(post, ['total', 'discount_sum', 'sub_total', 'vat_total', 'final_total', 'amount_paid'])
        date_convert(post, ['waybill_date', 'invoice_date', 'transaction_date', 'dispatch_date'])
        request.POST = post

    data = request.POST
    content = None
    table = None
    if pk is not None:
        try:
            table = model.objects.get(pk=pk)
            content = FinanceRecordContent.objects.filter(finance=table)
        except model.DoesNotExist:
            raise Http404("Does not exist")

        if request.method == "POST":
            form = form_class(data, instance=table)
            if form.is_valid():
                form.save()
                FinanceRecordContent.objects.filter(finance_id=pk).delete()
                if record_content:
                    FinanceRecordContent.objects.bulk_create(record_content)
                messages.success(request, 'Güncelleme başarılı.')
                return redirect('finance-record-list')
            else:
                messages.warning(request, 'Girilen bilgileri kontol ediniz.')
        else:
            form = form_class(instance=table)
    else:
        if request.method == "POST":
            form = form_class(data)
            if form.is_valid():
                form.save()
                if record_content:
                    FinanceRecordContent.objects.bulk_create(record_content)
                messages.success(request, 'Ekleme başarılı.')
                return redirect('finance-record-list')
            else:
                messages.warning(request, 'Girilen bilgileri kontol ediniz.')
        else:
            form = form_class()

    return render(request, template, {'form': form, 'table': table, 'pk': pk, 'content': content})


def finance_record_list(request):
    return crud_list(request, 'front_end/pages/list/finance_record.html', FinanceRecord)


def finance_record_delete(request, pk):
    return crud_delete(request, FinanceRecord, pk)
