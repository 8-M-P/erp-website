from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from .models import *


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    fieldsets = (
        ('Kullanıcı Bilgileri',
         {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('İzinler', {'fields': ('groups', 'user_permissions', 'is_staff', 'is_active')}),
        ('Şirket Bilgileri',
         {'fields': ('company_name', 'representative', 'website', 'tax_office', 'tax_no', 'about')}),
        ('İletişim Bilgileri', {'fields': ('phone_number_1', 'phone_number_2', 'mobil_phone_number', 'fax_number')}),
    )
    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


class CurrentGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(User, UserAdminConfig)
admin.site.register(CurrencyUnits)
admin.site.register(CurrentGroup, CurrentGroupAdmin)
admin.site.register(CurrentInformation)
admin.site.register(CurrentBankInformation)
admin.site.register(Media)
admin.site.register(FinanceRecord)
admin.site.register(FinanceRecordContent)
