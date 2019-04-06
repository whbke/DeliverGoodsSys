"""DeliverGoodsSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path

from DeliverGoods import views as  dg_views
from DeliverGoods import frontend_view as fd_views

urlpatterns = [
    # app
    path('admin/', admin.site.urls),
    path('dg/login', dg_views.do_login),
    path('dg/logout', dg_views.do_logout),
    path('dg/getCarInfo', dg_views.getCarInfo),
    path('dg/getShopNoteToday', dg_views.getShopNoteToday),
    path('dg/commitShopNote', dg_views.commitShopNote),

    # page
    re_path(r'^$', fd_views.index, name='index'),
    re_path(r'^login/$', fd_views.do_login, name='login'),
    re_path(r'^logout/$', fd_views.do_logout, name='logout'),

]
