from django.urls import path

from front_end.views.finance_record import testcontent, product_choose
from front_end.views.views import *

urlpatterns = [
    path('', current_group_list, name='home'),
    path('result', result, name='result'),
    path('test', testcontent),
    path('product-choose', product_choose, name='product-choose'),
]

# Current Group
urlpatterns += [
    path('current-group/', current_group_list, name='current-group-list'),
    path('current-group/create/', current_group, name='current-group-create'),
    path('current-group/<int:pk>/', current_group, name='current-group-update'),
    path('current-group/<int:pk>/delete/', current_group_delete, name='current-group-delete'),
]

# Current Info
urlpatterns += [
    path('current-info/', current_info_list, name='current-info-list'),
    path('current-info/create/', current_info, name='current-info-create'),
    path('current-info/<int:pk>/', current_info, name='current-info-update'),
    path('current-info/<int:pk>/delete/', current_info_delete, name='current-info-delete'),
]

# Current Bank Info
urlpatterns += [
    path('current-bank-info/', current_bank_info_list, name='current-bank-info-list'),
    path('current-bank-info/create/', current_bank_info, name='current-bank-info-create'),
    path('current-bank-info/<int:pk>/', current_bank_info, name='current-bank-info-update'),
    path('current-bank-info/<int:pk>/delete/', current_bank_info_delete, name='current-bank-info-delete'),
]

# Finance Record
urlpatterns += [
    path('finance-record/', finance_record_list, name='finance-record-list'),
    path('finance-record/create/', finance_record, name='finance-record-create'),
    path('finance-record/<int:pk>/', finance_record, name='finance-record-update'),
    path('finance-record/<int:pk>/delete/', finance_record_delete, name='finance-record-delete'),
]

# Finance Record Content
urlpatterns += [
    path('finance-record-content/choose/', finance_record_content_choose, name='finance-record-content-choose'),
    path('finance-record-content/create/', finance_record, name='finance-record-content-create'),
]

# Product
urlpatterns += [
    path('product/', product_list, name='product-list'),
    path('product/ajax/', product_list_ajax, name='product-list-ajax'),
    path('product/create/', product, name='product-create'),
    path('product/<int:pk>/', product, name='product-update'),
    path('product/<int:pk>/delete/', product_delete, name='product-delete'),
]

# Product Attribute
urlpatterns += [
    path('product-attr/', product_attr_list, name='product-attr-list'),
    path('product-attr/create/', product_attr, name='product-attr-create'),
    path('product-attr/<int:pk>/', product_attr, name='product-attr-update'),
    path('product-attr/<int:pk>/delete/', product_attr_delete, name='product-attr-delete'),
]

# Product Attribute Value
urlpatterns += [
    path('product-attr-value/', product_attr_value_list, name='product-attr-value-list'),
    path('product-attr-value/create/', product_attr_value, name='product-attr-value-create'),
    path('product-attr-value/<int:pk>/', product_attr_value, name='product-attr-value-update'),
    path('product-attr-value/<int:pk>/delete/', product_attr_value_delete, name='product-attr-value-delete'),
]

# Brand
urlpatterns += [
    path('brand/', brand_list, name='brand-list'),
    path('brand/create/', brand, name='brand-create'),
    path('brand/<int:pk>/', brand, name='brand-update'),
    path('brand/<int:pk>/delete/', brand_delete, name='brand-delete'),
]

# Category
urlpatterns += [
    path('category/', category_list, name='category-list'),
    path('category/create/', category, name='category-create'),
    path('category/<int:pk>/', category, name='category-update'),
    path('category/<int:pk>/delete/', category_delete, name='category-delete'),
]

# Stock
urlpatterns += [
    path('stock/', stock_list, name='stock-list'),
    path('stock/create/', stock, name='stock-create'),
    path('stock/<int:pk>/', stock, name='stock-update'),
    path('stock/<int:pk>/delete/', stock_delete, name='stock-delete'),
]
