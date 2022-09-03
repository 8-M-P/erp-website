from rest_framework.serializers import ModelSerializer

from accounting import models as account_models

from core import models as core_models


class WeightUnitsSerializer(ModelSerializer):
    class Meta:
        model = core_models.WeightUnits
        fields = '__all__'
        depth = 3


class CategorySerializer(ModelSerializer):
    class Meta:
        model = core_models.Category
        fields = '__all__'
        depth = 3


class BrandSerializer(ModelSerializer):
    class Meta:
        model = core_models.Brand
        fields = '__all__'
        depth = 3


class ProductAttributeSerializer(ModelSerializer):
    class Meta:
        model = core_models.ProductAttribute
        fields = '__all__'
        depth = 3


class ProductAttributeValueSerializer(ModelSerializer):
    class Meta:
        model = core_models.ProductAttributeValue
        fields = '__all__'
        depth = 3


class ProductSerializer(ModelSerializer):
    class Meta:
        model = core_models.Product
        fields = '__all__'
        depth = 3


class StockSerializer(ModelSerializer):
    class Meta:
        model = core_models.Stock
        fields = '__all__'
        depth = 3


class StockRecordSerializer(ModelSerializer):
    class Meta:
        model = core_models.StockRecord
        fields = '__all__'
        depth = 4


class ManufactureSerializer(ModelSerializer):
    class Meta:
        model = core_models.Manufacture
        fields = '__all__'
        depth = 3


class ProductMediaSerializer(ModelSerializer):
    class Meta:
        model = core_models.Media
        fields = '__all__'
        depth = 3


class CurrencyUnitsSerializer(ModelSerializer):
    class Meta:
        model = account_models.CurrencyUnits
        fields = '__all__'
        depth = 3


class CurrentGroupSerializer(ModelSerializer):
    class Meta:
        model = account_models.CurrentGroup
        fields = '__all__'
        depth = 3


class CurrentInformationSerializer(ModelSerializer):
    class Meta:
        model = account_models.CurrentInformation
        fields = '__all__'
        depth = 3


class CurrentBankInformationSerializer(ModelSerializer):
    class Meta:
        model = account_models.CurrentBankInformation
        fields = '__all__'
        depth = 3


class CurrentMediaSerializer(ModelSerializer):
    class Meta:
        model = account_models.Media
        fields = '__all__'
        depth = 3


class FinanceRecordSerializer(ModelSerializer):
    class Meta:
        model = account_models.FinanceRecord
        fields = '__all__'
        depth = 3


class FinanceRecordContentSerializer(ModelSerializer):
    class Meta:
        model = account_models.FinanceRecordContent
        fields = '__all__'
        depth = 3
