from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser
from django.contrib.auth.models import User
import os, json


JSON_PATH = 'mainapp/json_files'

def load_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **kwargs):
        categories = load_json('categories')
        ProductCategory.objects.all().delete()
        cats_dict = {}
        for cat in categories:
            new_cat = ProductCategory(**cat)
            new_cat.save()
            cats_dict[cat['name']] = new_cat.id

        products = load_json('products')
        Product.objects.all().delete()
        for product in products:
            # product['category_id'] = cats_dict[product['category']]
            cat_name = product['category']
            cat_obj = ProductCategory.objects.get(name=cat_name)
            product['category'] = cat_obj
            new_prod = Product(**product)
            new_prod.save()

        super_user = ShopUser.objects.create_superuser(
            'django',
            'django@geekbrains.local',
            'geekbrains',
            age=21
        )
