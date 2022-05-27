from statistics import mean

from sport_items.wsgi import *

from analitica.models import ETennis, GlobalTennis, TennisPro, DailyAnalytics, \
    WeeklyAnalytics, MonthlyAnalytics

from datetime import datetime, date, timedelta

class Analitica:

    def get_title(self, sku: dict) -> str:
        for key, value in sku.items():
            title = value.title
            return title

    def get_brand(self, sku: dict) -> str:
        for key, value in sku.items():
            brand = value.brand
            return brand

class DayAnalytic(Analitica):

    TABLES = (
        (ETennis, 'analitica_etennis'),
        (GlobalTennis, 'analitica_globaltennis'),
        (TennisPro, 'analitica_tennispro')
    )

    def get_data(self):
        data = {}
        for table in self.TABLES:
            queries = table[0].objects.all()
            info = {}
            for query in queries:
                sku = query.sku
                info[sku] = query
            data[table[1]] = info
        return data

    def sort_skus(self, data: dict):
        sort_sku = {}
        for shop in data:
            for sku in data[shop]:
                if sku in sort_sku:
                    sort_sku[sku][shop] = data[shop][sku]
                else:
                    sort_sku[sku] = {shop: data[shop][sku]}
        return sort_sku

    def make_data(self):
        data = self.get_data()
        sort_skus = self.sort_skus(data)
        n = 0
        for sku in sort_skus:
            information = self.get_data_for_save(sku, sort_skus[sku])
            self.save_data(information=information)

    def save_data(self, information: dict):
        analitica = DailyAnalytics(
            brand=information['brand'],
            sku=information['sku'],
            title=information['title'],
            best_price=information['best_price'],
            discount_e_tennis=information['discount_e_tennis'],
            discount_global_tennis=information['discount_global_tennis'],
            discount_tennis_pro=information['discount_tennis_pro'],
            price_e_tennis=information['price_e_tennis'],
            price_global_tennis=information['price_global_tennis'],
            price_tennis_pro=information['price_tennis_pro'],
            delete_from_e_tennis=information['delete_from_e_tennis'],
            delete_from_global_tennis=information['delete_from_global_tennis'],
            delete_from_tennis_pro=information['delete_from_tennis_pro'],
            new_from_e_tennis=information['new_from_e_tennis'],
            new_from_global_tennis=information['new_from_global_tennis'],
            new_from_tennis_pro=information['new_from_tennis_pro']
        )
        analitica.save()

    def get_data_for_save(self, sku: str, skus: dict) -> dict:
        information = {
            'best_price': self.get_best_price(skus),
            'sku': sku,
            'brand': self.get_brand(skus),
            'title': self.get_title(skus),
            'discount_e_tennis': self.get_prices(skus, 'analitica_etennis', 'discount'),
            'discount_global_tennis': self.get_prices(skus, 'analitica_globaltennis', 'discount'),
            'discount_tennis_pro': self.get_prices(skus, 'analitica_tennispro', 'discount'),
            'price_e_tennis': self.get_prices(skus, 'analitica_etennis', 'price'),
            'price_global_tennis': self.get_prices(skus, 'analitica_globaltennis', 'price'),
            'price_tennis_pro': self.get_prices(skus, 'analitica_tennispro', 'price'),
            'delete_from_e_tennis': self.get_delete_items(skus, 'analitica_etennis'),
            'delete_from_global_tennis': self.get_delete_items(skus, 'analitica_globaltennis'),
            'delete_from_tennis_pro': self.get_delete_items(skus, 'analitica_tennispro'),
            'new_from_e_tennis': self.get_new_items(skus, 'analitica_etennis'),
            'new_from_global_tennis': self.get_new_items(skus, 'analitica_globaltennis'),
            'new_from_tennis_pro': self.get_delete_items(skus, 'analitica_tennispro'),
        }
        return information

    def get_new_items(self, sku: dict, shop: str) -> bool:
        if shop in sku:
            data = datetime.date(datetime.now()) - sku[shop].data_create
            if data == timedelta(days=0):
                return True
        return False

    def get_delete_items(self, sku: dict, shop: str) -> bool:
        if shop in sku:
            data = datetime.date(datetime.now()) - sku[shop].data_update
            if data >= timedelta(days=1):
                return True
        return False

    def get_prices(self, sku: dict, table: str, type_price: str):
        if table in sku:
            if type_price == 'price':
                return sku[table].price
            return sku[table].discount
        return 0

    def get_best_price(self, sku: dict) -> float:
        price = {}
        for key, value in sku.items():
            if value.discount == 0:
                price[key] = value.price
            else:
                price[key] = value.discount
        min_price = min(price.values())
        return min_price

class WeekAnalytic(Analitica):

    def __init__(self):
        self.queries = DailyAnalytics.objects.filter(data_create__gte=date.today()-timedelta(days=7))
        self.table = WeeklyAnalytics

    def get_data(self) -> dict:
        data = {}
        for query in self.queries:
            if query.sku in data:
                data[query.sku][str(query.data_create)] = query
            else:
                data[query.sku] = {str(query.data_create): query}
        return data

    def make_data(self):
        data = self.get_data()
        for sku in data:
            information = self.get_data_for_save(sku, data[sku])
            self.save_data(information=information)

    def get_data_for_save(self, sku: str, skus: dict) -> dict:
        information = {
            'best_avr_price': self.get_prices(skus, 'best_avr_price'),
            'sku': sku,
            'brand': self.get_brand(skus),
            'title': self.get_title(skus),
            'avr_discount_e_tennis': self.get_prices(skus, 'analitica_etennis', 'discount'),
            'avr_discount_global_tennis': self.get_prices(skus, 'analitica_globaltennis', 'discount'),
            'avr_discount_tennis_pro': self.get_prices(skus, 'analitica_tennispro', 'discount'),
            'avr_price_e_tennis': self.get_prices(skus, 'analitica_etennis', 'price'),
            'avr_price_global_tennis': self.get_prices(skus, 'analitica_globaltennis', 'price'),
            'avr_price_tennis_pro': self.get_prices(skus, 'analitica_tennispro', 'price'),
            'delete_from_e_tennis': self.get_delete_items(skus, 'analitica_etennis'),
            'delete_from_global_tennis': self.get_delete_items(skus, 'analitica_globaltennis'),
            'delete_from_tennis_pro': self.get_delete_items(skus, 'analitica_tennispro'),
            'new_from_e_tennis': self.get_new_items(skus, 'analitica_etennis'),
            'new_from_global_tennis': self.get_new_items(skus, 'analitica_globaltennis'),
            'new_from_tennis_pro': self.get_delete_items(skus, 'analitica_tennispro'),
            'min_price_e_tennis': self.get_prices(skus, 'analitica_etennis', 'min'),
            'max_price_e_tennis': self.get_prices(skus, 'analitica_etennis', 'max'),
            'min_price_global_tennis': self.get_prices(skus, 'analitica_globaltennis', 'min'),
            'max_price_global_tennis': self.get_prices(skus, 'analitica_globaltennis', 'max'),
            'min_price_tennis_pro': self.get_prices(skus, 'analitica_tennispro', 'min'),
            'max_price_tennis_pro': self.get_prices(skus, 'analitica_tennispro', 'max'),
            'change_price_percent_e_tennis': self.get_prices(skus, 'analitica_etennis'),
            'change_price_percent_global_tennis': self.get_prices(skus, 'analitica_globaltennis'),
            'change_price_percent_tennis_pro': self.get_prices(skus, 'analitica_tennispro'),
        }
        return information

    def get_delete_items(self, sku: dict, column: str) -> bool:
        n = 0
        for i in sku:
            if column == 'analitica_etennis':
                info = sku[i].delete_from_e_tennis
            elif column == 'analitica_globaltennis':
                info = sku[i].delete_from_global_tennis
            else:
                info = sku[i].delete_from_tennis_pro
            if info is True:
                n += 1
            if n == 2:
                return True
        return False

    def get_prices(self, sku: dict, column: str, type_price: str = 'change'):
        price = {}
        just_price = []
        for key, value in sku.items():
            if column == 'analitica_etennis':
                if type_price == 'discount':
                    price[key] = value.discount_e_tennis
                    just_price.append(value.discount_e_tennis)
                else:
                    price[key] = value.price_e_tennis
                    just_price.append(value.price_e_tennis)
            elif column == 'best_avr_price':
                price[key] = value.best_price
                just_price.append(value.best_price)
            elif column == 'analitica_globaltennis':
                if type_price == 'discount':
                    price[key] = value.discount_global_tennis
                    just_price.append(value.discount_global_tennis)
                else:
                    price[key] = value.price_global_tennis
                    just_price.append(value.price_global_tennis)
            else:
                if type_price == 'discount':
                    just_price.append(value.discount_tennis_pro)
                    price[key] = value.discount_tennis_pro
                else:
                    price[key] = value.price_tennis_pro
                    just_price.append(value.price_tennis_pro)
        max_p = self.get_max_price(price)
        min_p = self.get_min_price(price)
        if type_price == 'min':
            return min_p
        elif type_price == 'max':
            return max_p
        elif type_price == 'price' or type_price == 'discount' or column == 'best_avr_price':
            list_avg = mean(just_price)
            return round(list_avg, 3)
        else:
            rezult = self.get_percent(max_p=max_p, min_p=min_p, price=price)
            return rezult

    def get_max_price(self, price: dict):
        if price:
            return max(price.values())
        return 0

    def get_min_price(self, price: dict):
        if price:
            return min(price.values())
        return 0

    def get_percent(self, max_p: float, min_p: float, price: dict):
        if max_p == min_p:
            return 0
        if max_p != 0 or min_p != 0:
            max_val = max(price, key=price.get)
            min_val = min(price, key=price.get)
            if max_val > min_val:
                if min_p == 0:
                    return 100
                percent = (max_p-min_p) / (min_p / 100)
                return percent
            if max_p == 0:
                return 100
            percent = (min_p - max_p) / (max_p / 100)
            return percent

    def get_new_items(self, sku: dict, column: str) -> bool:
        for i in sku:
            if column == 'analitica_etennis':
                info = sku[i].new_from_e_tennis
            elif column == 'analitica_globaltennis':
                info = sku[i].new_from_global_tennis
            else:
                info = sku[i].new_from_tennis_pro
            if info is True:
                return True
        return False

    def save_data(self, information: dict):
        analitica = self.table(
            brand=information['brand'],
            sku=information['sku'],
            title=information['title'],
            best_avr_price=information['best_avr_price'],
            avr_discount_e_tennis=information['avr_discount_e_tennis'],
            avr_discount_global_tennis=information['avr_discount_global_tennis'],
            avr_discount_tennis_pro=information['avr_discount_tennis_pro'],
            avr_price_e_tennis=information['avr_price_e_tennis'],
            avr_price_global_tennis=information['avr_price_global_tennis'],
            avr_price_tennis_pro=information['avr_price_tennis_pro'],
            delete_from_e_tennis=information['delete_from_e_tennis'],
            delete_from_global_tennis=information['delete_from_global_tennis'],
            delete_from_tennis_pro=information['delete_from_tennis_pro'],
            new_from_e_tennis=information['new_from_e_tennis'],
            new_from_global_tennis=information['new_from_global_tennis'],
            new_from_tennis_pro=information['new_from_tennis_pro'],
            min_price_e_tennis=information['min_price_e_tennis'],
            max_price_e_tennis=information['max_price_e_tennis'],
            min_price_global_tennis=information['min_price_global_tennis'],
            max_price_global_tennis=information['max_price_global_tennis'],
            min_price_tennis_pro=information['min_price_tennis_pro'],
            max_price_tennis_pro=information['max_price_tennis_pro'],
            change_price_percent_e_tennis=information['change_price_percent_e_tennis'],
            change_price_percent_global_tennis=information['change_price_percent_global_tennis'],
            change_price_percent_tennis_pro=information['change_price_percent_tennis_pro'],
            )
        analitica.save()

class MonthAnalytic(WeekAnalytic):

    def __init__(self):
        super().__init__()
        self.queries = DailyAnalytics.objects.filter(data_create__gte=date.today()-timedelta(days=30))
        self.table = MonthlyAnalytics


# i = Month()
# i.make_data()
