from django.contrib.auth.models import User, Permission
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices

from shopapp.views import TestingView
from shopapp.utils import multiplication_two_numbers
from shopapp.models import Product, Order


class MultiplicationTwoNumbersTestCase(TestCase):
    def test_multiplication_two_numbers(self):
        result = multiplication_two_numbers(5, 6)
        self.assertEqual(result, 30)


class TestingViewTestCase(TestCase):
    def test_testing_view(self):
        response = self.client.get(reverse('shopapp:test'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        expected_data = {'я': 'мыслю', 'следовательно': 'существую'}
        self.assertJSONEqual(response.content, expected_data)

class ProductCreateViewTestView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='sergei', password='Qawsed123')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        permission = Permission.objects.get(codename='add_product')
        self.user.user_permissions.add(permission)
        self.product_name = ''.join(choices(ascii_letters, k=6))
        Product.objects.filter(name=self.product_name).delete()
    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                'name': self.product_name,
                'price': '21',
                'description': 'Good Table',
                'discount': '10',
                'created_by': '1',
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name='Best Product')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    # проверка страницы и статус-кода
    def test_get_product(self):
        response = self.client.get(reverse('shopapp:product_details', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
    # проверка статус-кода и создания продукта
    def test_get_product_and_check_content(self):
        response = self.client.get(reverse('shopapp:product_details', kwargs={'pk': self.product.pk}))
        self.assertContains(response, self.product.name)

class OrderDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='sergei', password='Qawsed123')

    def setUp(self) -> None:
        self.client.force_login(self.user)
        permission = Permission.objects.get(codename='view_order')
        self.user.user_permissions.add(permission)
        self.order = Order.objects.create(
            delivery_address='Test Address',
            promocode='Test Promocode',
            user=self.user,
        )
    def tearDown(self) -> None:
        self.order.delete()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_detail', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertTrue(Order.objects.filter(pk=1).exists())

class OrdersExportViewTestCase(TestCase):
    fixtures = [
        'users-fixtures.json',
        'products-fixture.json',
        'orders-fixtures.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with transaction.atomic():
            cls.user = User.objects.create_user(username='sergey', password='Qawsed123', is_staff=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.id,
                'products': [
                    [
                        product.id,
                        product.name
                    ]
                    for product in order.products.all()
        ]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(orders_data['orders'], expected_data)



