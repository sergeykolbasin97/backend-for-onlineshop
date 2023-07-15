from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Выбор полей")
        # user_info = User.objects.values_list('username', flat=True)
        # print(list(user_info))

        user_info = User.objects.values_list('pk', 'username', 'email')
        print(user_info)
        for i_user in user_info:
            print(i_user)

        user_info2 = User.objects.only('pk', 'username', 'email').all()
        for i_user in user_info2:
            print(i_user.get_full_name())
        # product_values = Product.objects.values('pk', 'name', 'description')  # загружаем поля pk и name со всех товаров
        # print(product_values)
        # for i_product in product_values:
        #     print(i_product)
        self.stdout.write(f"Выполнено")
