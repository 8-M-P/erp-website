from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

import core.models


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="E-Posta", help_text="E-posta adresi.")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="İsim", help_text="Kullanıcı ismi.")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Soyisim", help_text="Kullanıcı soyismi.")
    start_date = models.DateTimeField(default=now, verbose_name="Oluşturma Tarihi", help_text="Hesabı yaratma tarihi.")
    is_staff = models.BooleanField(default=False, verbose_name="Yetkili mi ?",
                                   help_text="Bu hesap site yetkisine sahip mi ?.")
    is_active = models.BooleanField(default=False, verbose_name="Aktif mi ?",
                                    help_text="Hesap kullanılabilirlik durumu.")
    # Custom Fields
    company_name = models.CharField(max_length=50, blank=True, verbose_name="Şirket Adı",
                                    help_text="Şirket ticari sicil adı.")
    representative = models.CharField(max_length=50, blank=True, verbose_name="Şirket Temsilcisi",
                                      help_text="Şirket temsilcisi yada sahibi.")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Telefon numarası biçimi: '+2123237799'. En fazla 15 karekter.")
    phone_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                      verbose_name="Telefon Numarası (1)", help_text="Telefon Numarası (1).")
    phone_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                      verbose_name="Telefon Numarası (2)", help_text="Telefon Numarası (2).")
    mobil_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                          verbose_name="Cep Telefon Numarası", help_text="Cep Telefon Numarası.")
    fax_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                  verbose_name="Faks Numarası (2)", help_text="Faks Numarası.")
    website = models.URLField(blank=True, verbose_name="İnternet Sitesi",
                              help_text="örn: https://sirket.com.")
    tax_office = models.CharField(blank=True, max_length=50, verbose_name="Vergi Dairesi",
                                  help_text="Şirketin bağlı bulunduğu vergi dairesi.")
    tax_no = models.CharField(blank=True, max_length=50, verbose_name="Vergi Numarası",
                              help_text="Şirket vergi numarası.")
    about = models.TextField(max_length=500, blank=True, verbose_name="Kısa Bilgisi",
                             help_text="Şirket hakkında kısa bilgi.")

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"


class CurrencyUnits(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Birim Adı")
    symbol = models.CharField(max_length=5, unique=True, verbose_name="Sembol")
    shortening = models.CharField(max_length=5, unique=True, verbose_name="Kısaltma")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Para Birimi"
        verbose_name_plural = "Para Birimleri"


class CurrentGroup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Cari Grup Adı")
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Durum")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="children", null=True, blank=True,
                               verbose_name="Üst Grup", help_text="Alt grup ise zorunludur.")

    class Meta:
        ordering = ["name"]
        verbose_name = "Cari Grup"
        verbose_name_plural = "Cari Gruplar"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('current-group-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CurrentGroup, self).save(*args, **kwargs)


class CurrentInformation(models.Model):
    current_code = models.CharField(max_length=50, verbose_name="Cari Kodu")
    current_group = models.ForeignKey(CurrentGroup, on_delete=models.CASCADE, verbose_name="Cari Grup")
    current_name = models.CharField(max_length=50, blank=True, verbose_name="Şirket Adı",
                                    help_text="Şirket adı.")
    representative = models.CharField(max_length=50, blank=True, verbose_name="Şirket Temsilcisi",
                                      help_text="Şirket temsilcisi yada sahibi.")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Telefon numarası biçimi: '+2123237799'. En fazla 15 karekter.")
    phone_number_1 = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                      verbose_name="Telefon Numarası (1)")
    phone_number_2 = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                      verbose_name="Telefon Numarası (2)")
    mobil_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                                          verbose_name="Cep Telefon Numarası")
    fax_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Faks Numarası")
    website = models.URLField(blank=True, verbose_name="İnternet Sitesi",
                              help_text="örn: https://sirket.com.")
    tax_office = models.CharField(blank=True, max_length=50, verbose_name="Vergi Dairesi",
                                  help_text="Şirketin bağlı bulunduğu vergi dairesi.")
    tax_no = models.CharField(blank=True, max_length=50, verbose_name="Vergi Numarası",
                              help_text="Şirket vergi numarası.")
    about = models.TextField(max_length=500, blank=True, verbose_name="Kısa Bilgisi",
                             help_text="Şirket hakkında kısa bilgi.")
    purchase_discount = models.IntegerField(blank=True, null=True, verbose_name="Vergi Numarası",
                                            help_text="Şirket vergi numarası.")
    sale_discount = models.IntegerField(blank=True, null=True, verbose_name="Vergi Numarası",
                                        help_text="Şirket vergi numarası.")

    invoice_title = models.CharField(max_length=50, blank=True, verbose_name="Fatura Ünvanı",
                                     help_text="Ticari sicil adı.")
    city = models.CharField(max_length=50, blank=True, verbose_name="İl",
                            help_text="Şirket'in bulunduğu il.")
    district = models.CharField(max_length=50, blank=True, verbose_name="İlçe",
                                help_text="Şirket'in bulunduğu ilçe.")
    address = models.TextField(blank=True, verbose_name="Açık Adres", help_text="Şirket merkezi adresi.")
    PAYMENT_DAY = [
        (1, 'Pazartesi'),
        (2, 'Salı'),
        (3, 'Çarşamba'),
        (4, 'Perşembe'),
        (5, 'Cuma'),
        (6, 'Cumartesi'),
        (7, 'Pazar'),
    ]
    payment_day = models.IntegerField(default=1, blank=True, choices=PAYMENT_DAY, verbose_name="Ödeme Günü")

    class Meta:
        verbose_name = "Cari Hesap"
        verbose_name_plural = "Cari Hesaplar"

    def __str__(self):
        return self.current_name


class CurrentBankInformation(models.Model):
    current_information = models.ForeignKey(CurrentInformation, on_delete=models.CASCADE,
                                            verbose_name="Hesap Bilgileri")
    bank_name = models.CharField(max_length=50, verbose_name="Banka Adı", help_text="Banka ünvanı.")
    bank_branch_no = models.CharField(max_length=50, verbose_name="Şube Numarası", help_text="Banka şube numarası.")
    account_no = models.CharField(max_length=50, verbose_name="Hesap numarası", help_text="Hesap numarası.")
    account_title = models.CharField(max_length=50, verbose_name="Hesap Adı", help_text="Hesap sahibi ünvanı.")
    currency = models.ForeignKey(CurrencyUnits, on_delete=models.PROTECT, verbose_name="Para Birimi",
                                 help_text="Hesap para birimi.")

    class Meta:
        verbose_name = "Banka Bilgisi"
        verbose_name_plural = "Banka Bilgileri"


class Media(models.Model):
    current = models.ForeignKey(CurrentInformation, on_delete=models.CASCADE, verbose_name="Cari Hesap")
    img_url = models.ImageField()
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cari Resim"
        verbose_name_plural = "Cari Resimler"

    def __str__(self):
        return self.current.current_name


class FinanceRecord(models.Model):
    TRANSACTION_TYPE = [
        ('Alış İşlemleri', (
            (11, 'Peşin / Vadeli'),
            (12, 'Taksitli'),
            (13, 'İade'),
        )
         ),
        ('Satış İşlemleri', (
            (21, 'Peşin / Vadeli'),
            (22, 'Taksitli'),
            (23, 'İade'),
        )
         ),
        (31, 'Ödeme'),
        (41, 'Tahsilat'),
    ]
    PAYMENT_TYPE = [
        (1, 'Nakit'),
        (2, 'Açık Hesap'),
        (3, 'Kredi Kartı'),
        (4, 'Banka Hesabı'),
        (5, 'Çek'),
        (6, 'Senet'),
    ]
    INVOICE_TYPE = [
        (True, 'Açık'),
        (False, 'Kapalı'),
    ]
    current = models.ForeignKey(CurrentInformation, on_delete=models.PROTECT, verbose_name="Cari Hesap")
    transaction_date = models.DateField(default=now, verbose_name="İşlem Tarihi")
    transaction_type = models.IntegerField(default=11, choices=TRANSACTION_TYPE,
                                           verbose_name="İşlem Tipi")
    payment_type = models.IntegerField(choices=PAYMENT_TYPE, default=1, verbose_name="Ödeme Tipi")
    document_no = models.CharField(max_length=50, blank=True, verbose_name="Belge No")
    desc = models.TextField(blank=True, verbose_name="Açıklama")
    invoice_no = models.CharField(max_length=50, verbose_name="Fatura No")
    invoice_date = models.DateField(default=now, blank=True, null=True, verbose_name="Fatura Tarihi")
    invoice_type = models.BooleanField(choices=INVOICE_TYPE, default=False, verbose_name="Fatura Tipi")
    waybill_no = models.CharField(max_length=50, verbose_name="İrsaliye No")
    waybill_date = models.DateField(default=now, blank=True, null=True, verbose_name="İrsaliye Tarihi")
    dispatch_date = models.DateField(default=now, blank=True, null=True, verbose_name="Sevk Tarihi")
    total = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2,
                                verbose_name="İşlem Toplam Turaı", help_text="Fatura birimleri toplam turarı.")
    discount_sum = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2,
                                       verbose_name="İskonto Tutarı")
    sub_total = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2, verbose_name="Ara Toplam",
                                    help_text="İskonto uygulanmış tutar.")
    vat_total = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2, verbose_name="KDV Tutarı")
    final_total = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2,
                                      verbose_name="Genel Toplam", help_text="Fatura toplam tutarı.")
    amount_paid = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2,
                                      verbose_name="Ödenen Miktar", help_text="Faturanın kalan miktar.")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Finanslar Kayıt"
        verbose_name_plural = "Finanslar Kayıtlar"


class FinanceRecordContent(models.Model):
    finance = models.ForeignKey(FinanceRecord, on_delete=models.CASCADE, verbose_name="Cari Hesap")
    product = models.ForeignKey(core.models.Product, on_delete=models.PROTECT, verbose_name="Ürün")
    discount_rate = models.DecimalField(default=0, blank=True, max_digits=3, decimal_places=1,
                                        verbose_name="İskonto Oranı")
    quantity = models.DecimalField(default=0, blank=True, max_digits=3, decimal_places=1,
                                   verbose_name="Miktar")
    unit_price = models.DecimalField(default=0, blank=True, max_digits=9, decimal_places=2,
                                     verbose_name="Birim Fiyatı")

    def tax_sum(self):
        return (self.product.tax_rate / 100 * (self.discount_rate / 100 * self.unit_price)) * self.quantity

    def discount_sum(self):
        return (self.discount_rate / 100 * self.unit_price) * self.quantity

    def sum_total(self):
        return self.unit_price * self.quantity

    class Meta:
        verbose_name = "Finanslar Kayıt İçeriği"
        verbose_name_plural = "Finanslar Kayıt İçerikleri"
