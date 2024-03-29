"""
URL configuration for crypto_payments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path 
from payment_webpage import views

urlpatterns = [ 
    path("admin/", admin.site.urls),
    path("",views.homepage),
    path("qr_code",views.qr_code), 
    path("autopayment",views.start_autopayment),
    path("autopayment_trx",views.start_autopayment_trx),
    path("qr_code_trx",views.qr_code_trx),
    path("success_page",views.success_page),   
    #path("",views.pages_login),
    path("pages_register",views.pages_register),
    path("pages-error-404",views.error_page),
    re_path(r'^.*$',views.error_page)
]
