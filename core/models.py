from django.db import models
from django.db.models import Q, F, CheckConstraint
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class WeightUnits(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Adı")
    symbol = models.CharField(max_length=5, unique=True, verbose_name="Sembol")
    description = models.TextField(blank=True, verbose_name="Kısa Açıklama")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Ağırlık Birimi"
        verbose_name_plural = "Ağırlık Birimleri"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Durum")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="children", null=True, blank=True,
                               verbose_name="Üst Kategori", help_text="Alt kategori ise zorunludur.")

    class Meta:
        ordering = ["name"]
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Marka İsmi", help_text="Ürün markası")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"


class ProductAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Özellik Adı")
    description = models.TextField(blank=True, verbose_name="Kısa Açıklama")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ürün Özellikleri"
        verbose_name_plural = "Ürün Özellikleri"


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, verbose_name="Özellik")
    attribute_value = models.CharField(max_length=255, verbose_name="Değer")

    def __str__(self):
        return self.product_attribute.name + " : " + self.attribute_value

    class Meta:
        verbose_name = "Ürün Özellik Değeri"
        verbose_name_plural = "Ürün Özellik Değerleri"
        constraints = [
            models.UniqueConstraint(fields=['product_attribute', 'attribute_value'], name='unique_attr_value'),
        ]


class Product(models.Model):
    # web_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, verbose_name="İsim")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Açıklama")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Kategori")
    measurement_unit = models.ForeignKey(WeightUnits, on_delete=models.PROTECT, verbose_name="Ölçü Birimi")
    sku = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Stok Kodu",
                           verbose_name="Stok Kodu")
    upc = models.CharField(max_length=12, unique=True, blank=True, null=True, help_text="Barkod", verbose_name="Barkod")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Marka")
    attribute_values = models.ManyToManyField(ProductAttributeValue, blank=True,
                                              related_name="product_attribute_values", verbose_name="Özellikler")
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2, blank=True, null=True,
                                help_text="Ürün Fiyatı", verbose_name="Fiyat")
    tax_rate = models.CharField(default=0, max_length=2, blank=True, help_text="Ürün vergi oranı",
                                verbose_name="Vergi Oranı")
    is_active = models.BooleanField(default=True, verbose_name="Durum")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def save(self, *args, **kwargs):
        is_new = self.id is None
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
        if is_new:
            Stock.objects.create(product=self)


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, verbose_name="Ürün")
    last_checked = models.DateTimeField(default=now, blank=True, verbose_name="Son Kontrol Tarihi")
    units = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name="Birim")

    class Meta:
        verbose_name = "Stok"
        verbose_name_plural = "Stoklar"

    def __str__(self):
        return self.product.name + " : " + str(self.units)

    def save(self, *args, **kwargs):
        is_new = self.id is None
        if not is_new:
            last_units_count = Stock.objects.get(pk=self.pk)
            record_type = 1
            if last_units_count.units > self.units:
                record_type = 2
            StockRecord.objects.create(stock=self, prev_units=last_units_count.units, new_units=self.units,
                                       transaction_type=record_type)
        super(Stock, self).save(*args, **kwargs)


class StockRecord(models.Model):
    RECORD_TYPE = [
        (1, 'Ekleme'),
        (2, 'Çıkarma'),
    ]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="Stok")
    new_units = models.IntegerField(default=0, verbose_name="Yeni Birim")
    prev_units = models.IntegerField(default=0, verbose_name="Eski Birim")
    transaction_type = models.IntegerField(default=1, choices=RECORD_TYPE, verbose_name="İşlem Tipi")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stok Kayıt Bilgisi"
        verbose_name_plural = "Stok Kayıtları"

    def __str__(self):
        return self.stock.product.name + " : " + str(
            self.new_units) + " ( " + self.get_transaction_type_display() + " )"


class Manufacture(models.Model):
    raw_materials = models.ManyToManyField(Product, related_name="raw_materials", verbose_name="Hammadde(ler)")
    manufactured_product = models.ManyToManyField(Product, related_name="manufactured_product",
                                                  verbose_name="Üretilen Ürün(ler)")
    raw_materials_rates = models.JSONField(verbose_name="Hammadde(ler) oran(ları)")
    manufactured_product_rates = models.JSONField(verbose_name="Üretilen Ürün(ler) oran(ları)")
    raw_materials_weight = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                               help_text="Toplam kullanılan hammadde miktarı.(KG)",
                                               verbose_name="Hammadde Miktarı")
    manufactured_product_weight = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                                      help_text="Toplam üretilen ürün miktarı.(KG)",
                                                      verbose_name="Üretilen Miktarı")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Üretim Bilgisi"
        verbose_name_plural = "Üretim Kayıtları"


class Media(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün")
    img_url = models.ImageField()
    alt_text = models.CharField(max_length=255, blank=True)
    is_feature = models.BooleanField(default=False, verbose_name="Vitrin")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resim"
        verbose_name_plural = "Resimler"

    def __str__(self):
        return self.product.name
