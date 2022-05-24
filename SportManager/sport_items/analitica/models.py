from django.db import models


class ETennis(models.Model):
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True)
    data_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    is_sku = models.BooleanField(default=False)
    brand = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['price', 'brand', 'title']


class GlobalTennis(models.Model):
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True)
    data_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    is_sku = models.BooleanField(default=False)
    brand = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['price', 'brand', 'title']


class TennisPro(models.Model):
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True)
    data_create = models.DateField(auto_now_add=True)
    data_update = models.DateField(auto_now=True)
    is_sku = models.BooleanField(default=False)
    brand = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    sport_type = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['price', 'brand', 'title']


class DailyAnalytics (models.Model):
    brand = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    best_price = models.FloatField(blank=True)
    discount_e_tennis = models.FloatField(blank=True)
    discount_global_tennis = models.FloatField(blank=True)
    discount_tennis_pro = models.FloatField(blank=True)
    price_e_tennis = models.FloatField(blank=True)
    price_global_tennis = models.FloatField(blank=True)
    price_tennis_pro = models.FloatField(blank=True)
    delete_from_e_tennis = models.BooleanField(default=False)
    delete_from_global_tennis = models.BooleanField(default=False)
    delete_from_tennis_pro = models.BooleanField(default=False)
    new_from_e_tennis = models.BooleanField(default=False)
    new_from_global_tennis = models.BooleanField(default=False)
    new_from_tennis_pro = models.BooleanField(default=False)
    data_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['best_price', 'brand', 'title']


class WeeklyAnalytics (models.Model):
    brand = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    best_avr_price = models.FloatField(blank=True)
    avr_discount_e_tennis = models.FloatField(blank=True)
    avr_discount_global_tennis = models.FloatField(blank=True)
    avr_discount_tennis_pro = models.FloatField(blank=True)
    avr_price_e_tennis = models.FloatField(blank=True)
    min_price_e_tennis = models.FloatField(blank=True)
    max_price_e_tennis = models.FloatField(blank=True)
    change_price_percent_e_tennis = models.CharField(max_length=255)
    avr_price_global_tennis = models.FloatField(blank=True)
    min_price_global_tennis = models.FloatField(blank=True)
    max_price_global_tennis = models.FloatField(blank=True)
    change_price_percent_global_tennis = models.CharField(max_length=255)
    avr_price_tennis_pro = models.FloatField(blank=True)
    min_price_tennis_pro = models.FloatField(blank=True)
    max_price_tennis_pro = models.FloatField(blank=True)
    change_price_percent_tennis_pro = models.CharField(max_length=255)
    delete_from_e_tennis = models.BooleanField(default=False)
    delete_from_global_tennis = models.BooleanField(default=False)
    delete_from_tennis_pro = models.BooleanField(default=False)
    new_from_e_tennis = models.BooleanField(default=False)
    new_from_global_tennis = models.BooleanField(default=False)
    new_from_tennis_pro = models.BooleanField(default=False)
    data_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['best_avr_price', 'brand', 'title']


class MonthlyAnalytics (models.Model):
    brand = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    best_avr_price = models.FloatField(blank=True)
    avr_discount_e_tennis = models.FloatField(blank=True)
    avr_discount_global_tennis = models.FloatField(blank=True)
    avr_discount_tennis_pro = models.FloatField(blank=True)
    avr_price_e_tennis = models.FloatField(blank=True)
    min_price_e_tennis = models.FloatField(blank=True)
    max_price_e_tennis = models.FloatField(blank=True)
    change_price_percent_e_tennis = models.CharField(max_length=255)
    avr_price_global_tennis = models.FloatField(blank=True)
    min_price_global_tennis = models.FloatField(blank=True)
    max_price_global_tennis = models.FloatField(blank=True)
    change_price_percent_global_tennis = models.CharField(max_length=255)
    avr_price_tennis_pro = models.FloatField(blank=True)
    min_price_tennis_pro = models.FloatField(blank=True)
    max_price_tennis_pro = models.FloatField(blank=True)
    change_price_percent_tennis_pro = models.CharField(max_length=255)
    delete_from_e_tennis = models.BooleanField(default=False)
    delete_from_global_tennis = models.BooleanField(default=False)
    delete_from_tennis_pro = models.BooleanField(default=False)
    new_from_e_tennis = models.BooleanField(default=False)
    new_from_global_tennis = models.BooleanField(default=False)
    new_from_tennis_pro = models.BooleanField(default=False)
    data_create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['best_avr_price', 'brand', 'title']
