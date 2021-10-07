from django.urls import path, re_path

import authapp.views as authapp_views


app_name = 'authapp'

urlpatterns = [
    re_path(r'^login/$', authapp_views.login, name='login'),
    re_path(r'^logout/$', authapp_views.logout, name='logout'),

    re_path(r'^register/$', authapp_views.register, name='register'),
    re_path(r'^edit/$', authapp_views.edit, name='edit'),

    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp_views.verify,
            name='verify'),
    # path('verify/<email>/<activation_key>'),
]