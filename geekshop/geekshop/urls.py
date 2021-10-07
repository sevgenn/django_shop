"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
# from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include

import mainapp.views as mainapp_views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include('adminapp.urls', namespace='admin')),
    re_path(r'^auth/', include('authapp.urls', namespace='auth')),
    path('', include('social_django.urls', namespace='social')),

    re_path(r'^$', mainapp_views.main, name='main'),
    re_path(r'^contacts/$', mainapp_views.contacts, name='contacts'),
    re_path(r'^products/', include('mainapp.urls', namespace='products')),
    re_path(r'^basket/', include('basketapp.urls', namespace='basket')),
    re_path(r'^order/', include('ordersapp.urls', namespace='order')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
