from django.contrib import admin
from django.apps import apps
from .models import *

# auto-register all models
app = apps.get_app_config('core')


class WeightUnitsAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'description')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active')


class WarehouseShelfAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'shelf', 'is_active')


class WarehouseRackAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse', 'get_shelf', 'rack', 'is_active')

    @admin.display(ordering='warehouse__name', description='Depo İsmi')
    def get_warehouse(self, obj):
        return obj.warehouse_shelf.warehouse.name

    @admin.display(ordering='shelf__name', description='Raf İsmi')
    def get_shelf(self, obj):
        return obj.warehouse_shelf.shelf


class WarehouseStockAdmin(admin.ModelAdmin):
    list_display = ('get_warehouse', 'get_shelf', 'get_rack', 'get_product', 'units', 'is_active')

    @admin.display(ordering='warehouse__name', description='Depo İsmi')
    def get_warehouse(self, obj):
        return obj.warehouse.name

    @admin.display(ordering='shelf__name', description='Raf İsmi')
    def get_shelf(self, obj):
        return obj.shelf.shelf

    @admin.display(ordering='rack__name', description='Raf Kat İsmi')
    def get_rack(self, obj):
        return obj.rack.rack

    @admin.display(ordering='product__name', description='Ürün İsmi')
    def get_product(self, obj):
        return obj.product.name


admin.site.register(WeightUnits, WeightUnitsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(StockRecord)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(WarehouseShelf, WarehouseShelfAdmin)
admin.site.register(WarehouseRack, WarehouseRackAdmin)
admin.site.register(WarehouseStock, WarehouseStockAdmin)
admin.site.register(WarehouseStockRecord)
admin.site.register(Manufacture)
admin.site.register(Media)

# for model_name, model in app.models.items():
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
