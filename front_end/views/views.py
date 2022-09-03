from django.shortcuts import render

from .current_group import current_group_list, current_group, current_group_delete
from .current_info import current_info_list, current_info, current_info_delete
from .current_bank_info import current_bank_info_list, current_bank_info, current_bank_info_delete
from .finance_record import finance_record_list, finance_record, finance_record_delete
from .product import product_list, product_list_ajax, product, product_delete
from .product_attr import product_attr_list, product_attr, product_attr_delete
from .product_attr_value import product_attr_value_list, product_attr_value, product_attr_value_delete
from .brand import brand_list, brand, brand_delete
from .category import category_list, category, category_delete
from .stock import stock_list, stock, stock_delete


def result(request):
    return render(request, 'front_end/widgets/result.html')
