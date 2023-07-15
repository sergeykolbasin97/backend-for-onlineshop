from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Создание записей")
        info = [
            ('Лампа', 345),
            ('Клавиатура', 345),
            ('Игрушка', 345)
        ]
        product_list = [
            Product(name=name, price=price)
            for name, price in info
        ]
        for i in product_list:
            print(dir(i))
        self.stdout.write(f"Выполнено")
