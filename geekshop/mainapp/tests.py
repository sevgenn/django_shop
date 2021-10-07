from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command


class TestMainappTestCase(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.expected_status_code = 200

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.expected_status_code)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, self.expected_status_code)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.expected_status_code)

        response = self.client.get('/products/category/1/')
        self.assertEqual(response.status_code, self.expected_status_code)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.expected_status_code)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.expected_status_code)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
