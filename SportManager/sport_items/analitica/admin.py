from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse

from .models import *


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class PriceFilter(admin.SimpleListFilter):
    title = 'range price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (('0', ('0-50')), ('51', ('50-100')), ('101', ('100-150')), ('151', ('150-200')),
                ("201", ('200-300')), ('301', ('300-400')), ('401', ('400-500')), ('501', ('500-1000000')))

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(price__gte=0, price__lt=50)
        if self.value() == '51':
            return queryset.filter(price__gte=50, price__lt=100)
        if self.value() == '101':
            return queryset.filter(price__gte=100, price__lt=150)
        if self.value() == '151':
            return queryset.filter(price__gte=150, price__lt=200)
        if self.value() == "201":
            return queryset.filter(price__gte=200, price__lt=300)
        if self.value() == '301':
            return queryset.filter(price__gte=301, price__lt=400)
        if self.value() == '401':
            return queryset.filter(price__gte=401, price__lt=500)
        if self.value() == '501':
            return queryset.filter(price__gte=501, price__lte=100000)


class DiscountFilter(admin.SimpleListFilter):
    title = 'discount'
    parameter_name = 'discount'

    def lookups(self, request, model_admin):
        return (('0', ('with discount')), ('1', ('without discount')))

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(discount=0)
        if self.value() == '1':
            return queryset.filter(discount__gt=0)


class BrandFilter(admin.SimpleListFilter):
    title = 'brand'
    parameter_name = 'brand'

    def lookups(self, request, model_admin):
        return (('0', ('A-E')), ('1', ('F-J')), ('2', ('K-O')), ('3', ('P-Z')))

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(brand__gte="A", brand__lt="E")
        if self.value() == '1':
            return queryset.filter(brand__gte='F', brand__lt='J')
        if self.value() == '2':
            return queryset.filter(brand__gte='K', brand__lt='O')
        if self.value() == '3':
            return queryset.filter(brand__gte='P')


class ETennisAdmin(admin.ModelAdmin):
    list_display = ('brand', 'title', 'sku', 'price', 'discount', 'product_type', 'sport_type',
                     'is_sku')
    list_display_links = ('brand', 'title', 'sku', 'price', 'discount', 'product_type', 'sport_type',
                     'is_sku')
    search_fields = ('brand', 'title', 'price', 'discount', 'product_type', 'sport_type',
                     'is_sku')
    list_filter = (PriceFilter, DiscountFilter, BrandFilter, 'product_type', 'sport_type',
                   'is_sku')
    actions = [export_to_csv]


class DailyAdmin(admin.ModelAdmin):
    list_display = ('brand', 'sku', 'title', 'best_price', 'avr_price', 'discount_e_tennis',
                    'price_e_tennis', 'change_percent_e_tennis', 'discount_global_tennis',
                    'price_global_tennis', 'change_percent_global_tennis', 'discount_tennis_pro',
                     'price_tennis_pro', 'change_percent_tennis_pro')
    list_display_links = ('brand', 'sku', 'title', 'best_price', 'avr_price', 'discount_e_tennis',
                    'price_e_tennis', 'change_percent_e_tennis', 'discount_global_tennis',
                    'price_global_tennis', 'change_percent_global_tennis', 'discount_tennis_pro',
                     'price_tennis_pro', 'change_percent_tennis_pro')
    search_fields = ('brand', 'sku', 'title', 'best_price', 'avr_price', 'discount_e_tennis',
                    'price_e_tennis', 'change_percent_e_tennis', 'discount_global_tennis',
                    'price_global_tennis', 'change_percent_global_tennis', 'discount_tennis_pro',
                     'price_tennis_pro', 'change_percent_tennis_pro')
    list_filter = (BrandFilter, 'data_create', 'delete_from_e_tennis',
                    'delete_from_global_tennis', 'delete_from_tennis_pro', 'new_from_e_tennis',
                    'new_from_global_tennis', 'new_from_tennis_pro')
    actions = [export_to_csv]


class WeeklyAdmin(admin.ModelAdmin):
    list_display = ('brand', 'sku', 'title', 'best_avr_price', 'avr_discount_e_tennis',
                    'avr_discount_global_tennis', 'avr_discount_tennis_pro', 'avr_price_e_tennis',
                    'avr_price_global_tennis', 'avr_price_tennis_pro')
    list_display_links = ('brand', 'sku', 'title', 'best_avr_price', 'avr_discount_e_tennis',
                    'avr_discount_global_tennis', 'avr_discount_tennis_pro', 'avr_price_e_tennis',
                    'avr_price_global_tennis', 'avr_price_tennis_pro')
    search_fields = ('brand', 'title', 'best_avr_price', 'avr_discount_e_tennis',
                    'avr_discount_global_tennis', 'avr_discount_tennis_pro', 'avr_price_e_tennis',
                    'avr_price_global_tennis', 'avr_price_tennis_pro')
    list_filter = (BrandFilter, 'data_create', 'delete_from_e_tennis',
                    'delete_from_global_tennis', 'delete_from_tennis_pro', 'new_from_e_tennis',
                    'new_from_global_tennis', 'new_from_tennis_pro')
    actions = [export_to_csv]


admin.site.register(ETennis, ETennisAdmin)
admin.site.register(GlobalTennis, ETennisAdmin)
admin.site.register(TennisPro, ETennisAdmin)
admin.site.register(DailyAnalytics, DailyAdmin)
admin.site.register(WeeklyAnalytics, WeeklyAdmin)
admin.site.register(MonthlyAnalytics, WeeklyAdmin)