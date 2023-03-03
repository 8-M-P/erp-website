from accounting.models import FinanceRecord, FinanceRecordContent, CurrentInformation
from core.models import Product
from front_end.forms import FinanceRecordForm
from front_end.utils.crud import crud, crud_list, crud_delete

import json
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
    print(products)
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
                'discount_sum': round(discount_sum),
                'sub_total': round(sub_total),
                'vat_total': round(vat_total),
                'total': round(total),
                'upc': product.get('upc'),
            },
            'public': {
                'sku': product.get('sku'),
                'name': product.get('name'),
                'measurement_unit': product.get('measurement_unit'),
                'tax_rate': product.get('tax_rate'),
                'discount_rate': product.get('discount_rate'),
                'quantity': product.get('quantity'),
                'unit_price': product.get('unit_price'),
                'final_total': round(final_total),
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
            'total': bill_result.get('total') + round(bill.get('hidden').get('total')),
            'discount_sum': bill_result.get('total') + round(bill.get('hidden').get('discount_sum')),
            'sub_total': bill_result.get('total') + round(bill.get('hidden').get('sub_total')),
            'vat_total': bill_result.get('total') + round(bill.get('hidden').get('vat_total')),
            'final_total': bill_result.get('total') + round(bill.get('public').get('final_total')),
        }
    print({'bill_result': bill_result, 'products_bills': product_bills})
    return JsonResponse({'bill_result': bill_result, 'products_bills': product_bills})


def product_choose(request):
    if request.method == "POST":
        data = request.body
        return bill_calc(data)
    return HttpResponseBadRequest()


def testcontent(request):
    res = '''
        <!DOCTYPE html>
        <html>
        <body onload="myFunction()">
        <div id="modalBody"></div>
        <h1>HTML DOM Events</h1>
        <h2>The onload Event</h2>
        
        <script>
        function myFunction() {
           fetch('test2').then(function (response) {
                return response.json();
            }).then(function (html) {
                document.getElementById("modalBody").innerHTML = html.bill_result;
                console.log(html.bill_result)
            }).catch(function (err) {
                console.warn('Something went wrong.', err);
            });
        }
        </script>
        
        </body>
        </html>'''
    return HttpResponse(res)
    # return json data ve tabloya ekle 


def finance_record_content_choose(request, current_pk=None, product_pk=None, finance_pk=None):
    finance_model = FinanceRecord
    finance_content_model = FinanceRecordContent
    product_model = Product
    if finance_pk is not None:
        try:
            finance_table = finance_model.objects.get(pk=finance_pk)
        except finance_model.DoesNotExist:
            raise Http404("Does not exist")
    else:
        finance_table = finance_model(current=CurrentInformation.objects.get(pk=current_pk))
        finance_table.save()

    if product_pk is not None:
        try:
            product_table = product_model.objects.get(pk=product_pk)
        except product_model.DoesNotExist:
            raise Http404("Does not exist")
    else:
        raise Http404("Does not exist")

    defaults = {
        'discount_rate': 20.0,
        'quantity': 1.0,
        'unit_price': product_table.price,
    }
    finance_content_table, created = finance_content_model.objects.update_or_create(
        finance=finance_table, product=product_table,
        defaults=defaults,
    )
    print(defaults)
    print(finance_content_table)
    print(created)
    return HttpResponse('selam')


def finance_record(request, pk=None):
    products = [
        {'pk': 2, 'tax_rate': 10.0, 'discount_rate': 20.0, 'quantity': 0.5, 'unit_price': 1000.00},
        {'pk': 3, 'tax_rate': 20.0, 'discount_rate': 30.0, 'quantity': 2.0, 'unit_price': 5000.00},
    ]

    record_content = []
    model = FinanceRecord
    form_class = FinanceRecordForm
    template = "front_end/pages/create_or_update/finance_record.html"
    if request.method == "POST":
        post = request.POST.copy()  # to make it mutable
        for index in range(len(post.getlist('data-product-id'))):
            product = FinanceRecordContent(finance=model.objects.get(pk=pk),
                                           product=Product.objects.get(pk=post.getlist('data-product-id')[index]),
                                           discount_rate=post.getlist('data-product-discount')[index],
                                           quantity=post.getlist('data-product-unit')[index],
                                           unit_price=post.getlist('data-product-price-by-unit')[index])
            record_content.append(product)

        post['total'] = float(post['total'].replace(',', '')) if post['total'] else post['total']
        post['discount_sum'] = float(post['discount_sum'].replace(',', '')) if post['discount_sum'] else post[
            'discount_sum']
        post['sub_total'] = float(post['sub_total'].replace(',', '')) if post['sub_total'] else post['sub_total']
        post['vat_total'] = float(post['vat_total'].replace(',', '')) if post['vat_total'] else post['vat_total']
        post['final_total'] = float(post['final_total'].replace(',', '')) if post['final_total'] else post[
            'final_total']
        post['amount_paid'] = float(post['amount_paid'].replace(',', '')) if post['amount_paid'] else post[
            'amount_paid']
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
