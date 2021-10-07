from django.urls import path, re_path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp_views


app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp_views.products, name='index'),
    re_path(r'^category/(?P<pk>\d+)/$', mainapp_views.products, name='category'),
    re_path(r'^category/(?P<pk>\d+)/ajax/$', cache_page(3600)(mainapp_views.products_ajax)),
    re_path('^product/(?P<pk>\d+)/$', mainapp_views.product, name='product'),
    re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp_views.products, name='page'),
    re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/ajax/$', cache_page(3600)(mainapp_views.products_ajax)),
]
