from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import json
import os
import random

from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache

from geekshop.settings import BASE_DIR
from django.conf import settings
from django.core.cache import cache

from mainapp.management.commands.fill_db import JSON_PATH
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk,
                                              is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products_list = Product.objects.filter(category__is_active=True, is_active=True)
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
     same_products = Product.objects.filter(category=hot_product.category, is_active=True).\
         exclude(pk=hot_product.pk)[:3]
     return same_products


def main(request):
    title = 'главная'
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):
    title = 'продукты'
    # links_menu = ProductCategory.objects.filter(is_active=True)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'hot_product': hot_product,
        'same_products': same_products,
    }

    if pk is not None:
        category = get_category(pk)
        products = Product.objects.filter(category__pk=pk, is_active=True,
                    category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['category'] = category
        context['products'] = products_paginator
        return render(request, 'mainapp/products_list.html', context)

    # same_products = []
    # products_path = os.path.join(BASE_DIR, 'mainapp/json_files/same_products.json')
    # if os.path.exists(products_path):
    #     with open(products_path, encoding='utf-8') as f:
    #         same_products = json.load(f)
    # same_products = Product.objects.all()[:3]

    # context['same_products'] = same_products
    return render(request, 'mainapp/products.html', context)


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()

    if pk is not None:
        category = get_category(pk)
        products = Product.objects.filter(category__pk=pk, is_active=True,
                    category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }

        result = render_to_string(
            'mainapp/includes/inc_products_list_content.html',
            context=context,
            request=request)

        return JsonResponse({'result': result})


def contacts(request):
    title = 'контакты'
    # location = []
    # location_path = os.path.join(BASE_DIR, 'mainapp/json_files/location.json')
    # if os.path.exists(location_path):
    #     with open(location_path, encoding='utf-8') as f:
    #         location = json.load(f)
    location = load_from_json('location')
    context = {
        'title': title,
        'location': location,
    }
    return render(request, 'mainapp/contacts.html', context)

# @never_cache
def product(request, pk):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'product': product,
        'links_menu': get_links_menu(),
    }
    return render(request, 'mainapp/product.html', context)
