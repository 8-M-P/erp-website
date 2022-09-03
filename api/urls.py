from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'weight-units', views.WeightUnitsViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'brand', views.BrandViewSet)
router.register(r'product-attribute', views.ProductAttributeViewSet)
router.register(r'product-attribute-value', views.ProductAttributeValueViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'stock', views.StockViewSet)
router.register(r'stock-record', views.StockRecordViewSet)
router.register(r'manufacture', views.ManufactureViewSet)
router.register(r'product-media', views.ProductMediaViewSet)
router.register(r'currency-units', views.CurrencyUnitsViewSet)
router.register(r'current-group', views.CurrentGroupViewSet)
router.register(r'current-information', views.CurrentInformationViewSet)
router.register(r'current-bankinformation', views.CurrentBankInformationViewSet)
router.register(r'current-media', views.CurrentMediaViewSet)
router.register(r'finance-record', views.FinanceRecordViewSet)
router.register(r'finance-record-content', views.FinanceRecordContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
