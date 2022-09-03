from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from core import models as core_models


class WeightUnitsViewSet(ModelViewSet):
    queryset = core_models.WeightUnits.objects.all()
    serializer_class = WeightUnitsSerializer


class CategoryViewSet(ModelViewSet):
    queryset = core_models.Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(ModelViewSet):
    queryset = core_models.Brand.objects.all()
    serializer_class = BrandSerializer


class ProductAttributeViewSet(ModelViewSet):
    queryset = core_models.ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductAttributeValueViewSet(ModelViewSet):
    queryset = core_models.ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer


class ProductViewSet(ModelViewSet):
    queryset = core_models.Product.objects.all()
    serializer_class = ProductSerializer


class StockViewSet(ModelViewSet):
    queryset = core_models.Stock.objects.all()
    serializer_class = StockSerializer


class StockRecordViewSet(ModelViewSet):
    queryset = core_models.StockRecord.objects.all()
    serializer_class = StockRecordSerializer


class ManufactureViewSet(ModelViewSet):
    queryset = core_models.Manufacture.objects.all()
    serializer_class = ManufactureSerializer


class ProductMediaViewSet(ModelViewSet):
    queryset = core_models.Media.objects.all()
    serializer_class = ProductMediaSerializer


class CurrencyUnitsViewSet(ModelViewSet):
    queryset = account_models.CurrencyUnits.objects.all()
    serializer_class = CurrencyUnitsSerializer


class CurrentGroupViewSet(ModelViewSet):
    queryset = account_models.CurrentGroup.objects.all()
    serializer_class = CurrentGroupSerializer


class CurrentInformationViewSet(ModelViewSet):
    queryset = account_models.CurrentInformation.objects.all()
    serializer_class = CurrentInformationSerializer


class CurrentBankInformationViewSet(ModelViewSet):
    queryset = account_models.CurrentBankInformation.objects.all()
    serializer_class = CurrentBankInformationSerializer


class CurrentMediaViewSet(ModelViewSet):
    queryset = account_models.Media.objects.all()
    serializer_class = CurrentMediaSerializer


class FinanceRecordViewSet(ModelViewSet):
    queryset = account_models.FinanceRecord.objects.all()
    serializer_class = FinanceRecordSerializer


class FinanceRecordContentViewSet(ModelViewSet):
    queryset = account_models.FinanceRecordContent.objects.all()
    serializer_class = FinanceRecordContentSerializer
