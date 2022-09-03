from django.contrib import admin
from django.apps import apps
from .models import *

# auto-register all models
app = apps.get_app_config('core')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(WeightUnits)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock)
admin.site.register(StockRecord)
admin.site.register(Manufacture)
admin.site.register(Media)

# for model_name, model in app.models.items():
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
