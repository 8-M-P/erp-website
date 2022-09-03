from django.forms import ModelForm

import accounting.models
import core.models


class CurrentGroupForm(ModelForm):
    class Meta:
        model = accounting.models.CurrentGroup
        fields = ['name', 'parent', 'is_active']


class CurrentInformationForm(ModelForm):
    class Meta:
        model = accounting.models.CurrentInformation
        fields = '__all__'


class CurrentBankInformationForm(ModelForm):
    class Meta:
        model = accounting.models.CurrentBankInformation
        fields = '__all__'


class FinanceRecordForm(ModelForm):
    class Meta:
        model = accounting.models.FinanceRecord
        fields = '__all__'


class BrandForm(ModelForm):
    class Meta:
        model = core.models.Brand
        fields = ['name']


class CategoryForm(ModelForm):
    class Meta:
        model = core.models.Category
        fields = ['name', 'parent', 'is_active']


class ProductForm(ModelForm):
    class Meta:
        model = core.models.Product
        fields = '__all__'


class ProductAttributeForm(ModelForm):
    class Meta:
        model = core.models.ProductAttribute
        fields = '__all__'


class ProductAttributeValueForm(ModelForm):
    class Meta:
        model = core.models.ProductAttributeValue
        fields = '__all__'


class StockForm(ModelForm):
    class Meta:
        model = core.models.Stock
        exclude = ['last_checked']
