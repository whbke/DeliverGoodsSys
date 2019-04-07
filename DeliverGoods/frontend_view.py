# -*- coding: UTF-8 -*-

import logging
import json
import datetime

from django.db.models import F
from django.http import response
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from DeliverGoods.forms import *
from django.contrib.auth import views as auth_views
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.db import models
from django.utils import timezone
from django.shortcuts import render, redirect

from DeliverGoods import models as dg_models


logger = logging.getLogger('DeliverGoods.frontend_view')


#登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username,password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request,'error.html',{'reason': '登录验证失败'})
                if request.POST.get('source_url') is None or request.POST.get('source_url') == '':
                    index(request)
                else:
                    return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'error.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    source_url = request.GET.get('source_url', '')
    return render(request, 'login.html', locals())

#退出
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())


# 首页
@login_required
def index(request):
    noteTime = request.GET.get('noteTime')
    if noteTime is None or noteTime == '':
        noteTime = timezone.now()
    else:
        noteTime = timezone.datetime.strptime(noteTime, "%Y-%m-%d")
    totalPrice = 0
    actualPrice = 0
    bookkeeping = 0
    carList = []
    for car in dg_models.Car.objects.all():
        carTotalPrice = 0
        carActualPrice = 0
        carBookkeeping = 0

        carInfo = {}
        carInfo['id'] = car.id
        carInfo['name'] = car.name
        carInfo['driver'] = car.driver.last_name
        # 车内剩余商品
        remainderGoodList = []
        for goodsItem in car.goods.all():
            remainderGoodList.append({
                'id': goodsItem.id,
                'name': goodsItem.goods.name,
                'goodsId': goodsItem.goods.id,
                'carCurrentNumber': goodsItem.carCurrentNumber,
                'carTargetNumber': goodsItem.carTargetNumber,
                'unitId': goodsItem.goods.unit.id,
                'unitName': goodsItem.goods.unit.name,
            })
        carInfo['remainderGoodList'] = remainderGoodList
        # 送货订单
        noteList = []
        for note in dg_models.DeliveryNote.objects.filter(shop_id__in=[shop.id for shop in car.route.shops.all()], noteTime=noteTime):
            totalPrice += note.totalPrice
            actualPrice += note.actualPrice
            bookkeeping += note.bookkeeping
            carTotalPrice += note.totalPrice
            carActualPrice += note.actualPrice
            carBookkeeping += note.bookkeeping
            noteInfo = {
                'id': note.id,
                'shopId': note.shop.id,
                'shopName': note.shop.name,
                'totalPrice': note.totalPrice,
                'actualPrice': note.actualPrice,
                'bookkeeping': note.bookkeeping,
            }
            noteGoodsList = []
            for noteGoodsItem in note.goods.all():
                noteGoodsList.append({
                    'id': noteGoodsItem.id,
                    'goodsId': noteGoodsItem.goods.goods.id,
                    'goodsName': noteGoodsItem.goods.goods.name,
                    'price': noteGoodsItem.goods.price,
                    'actualDeliveryNumber': noteGoodsItem.actualDeliveryNumber,
                    'unitName': noteGoodsItem.goods.goods.unit.name,
                    'amount': noteGoodsItem.goods.price * noteGoodsItem.actualDeliveryNumber
                })
            noteInfo['noteGoodsList'] = noteGoodsList
            noteList.append(noteInfo)
        carInfo['noteList'] = noteList
        carInfo['totalPrice'] = carTotalPrice
        carInfo['actualPrice'] = carActualPrice
        carInfo['bookkeeping'] = carBookkeeping
        carList.append(carInfo)
    return render(request, "index.html", locals())