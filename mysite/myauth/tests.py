from django.test import TestCase
from django.urls import reverse

from myauth.views import get_cookie_view

class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('myauth:cookie-get'))
        self.assertContains(response, 'Данные cookie')