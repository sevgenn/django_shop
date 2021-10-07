from django.urls import path

import basketapp.views as basketapp_views


app_name = 'basketapp'

urlpatterns = [
    path('', basketapp_views.basket, name='view'),
    path('add/<int:pk>/', basketapp_views.basket_add, name='add'),
    path('edit/<int:pk>/<int:quantity>/', basketapp_views.basket_edit, name='edit'),
    path('remove/<int:pk>/', basketapp_views.basket_remove, name='remove'),
]