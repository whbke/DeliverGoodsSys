import logging
import json
import datetime

from django.db.models import F
from django.http import response
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.db import models
from django.utils import timezone

from DeliverGoods import models as dg_models


logger = logging.getLogger('DeliverGoods.views')


class ResponseMsg(response.JsonResponse):
    def __init__(self, status, result=None, msg=None):
        if isinstance(result, QuerySet):
            if len(result) == 0:
                pass
            elif isinstance(result[0], models.Model):
                result = json.loads(serializers.serialize('json', result, cls=DjangoJSONEncoder))
            elif isinstance(result[0], dict):
                result = list(result);

        super(ResponseMsg, self).__init__({
            'status': status,
            'result': result,
            'msg': msg
        })


#登录
def do_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username,password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return ResponseMsg(True, {
                    'sessionid': request.session.session_key
                }, '登录成功')
            else:
                return ResponseMsg(False, None, '登录失败')
    except Exception as e:
        logger.error(e)
    return ResponseMsg(False, None, 'error')


#退出
def do_logout(request):
    try:
        logout(request)
        return ResponseMsg(True, None, 'success')
    except Exception as e:
        logger.error(e)
    return ResponseMsg(False, None, 'error')


@login_required
def getCarInfo(request):
    try:
        car_list = dg_models.Car.objects.filter(driver=request.user.id)
        if car_list is None or len(car_list) == 0:
            return ResponseMsg(False, None, '你不是司机')
        if len(car_list) > 1:
            return ResponseMsg(False, None, '你有多个路线，请联系系统管理员')
        car = car_list[0]
        if car.route is None:
            return ResponseMsg(False, None, '没有可用路线,请联系系统管理员')
        carInfo = {
            'id': car.id,
            'name': car.name,
            'dirver': {
                'id': car.driver.id,
                'name': car.driver.last_name
            },
            'route': {
                'id': car.route.id,
                'name': car.route.name,
                'shops': list(car.route.shops.all().values()),
            },
            'goods': [
                {
                    'carGoodsItemId': goodsItem.id,
                    'goodsId': goodsItem.goods.id,
                    'name': goodsItem.goods.name,
                    'currentNumber': goodsItem.carCurrentNumber,
                    'unitId': goodsItem.goods.unit.id,
                    'unitName': goodsItem.goods.unit.name,
                } for goodsItem in car.goods.all()
            ]
        }

        return ResponseMsg(True, carInfo, None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, '异常')


"""
获取订单模板
"""
@login_required
def getShopNoteToday(request):
    try:
        shop = dg_models.Shop.objects.get(pk=request.GET['shopId'])
        if shop is None:
            return ResponseMsg(False, None, '未知商家！')
        car = dg_models.Car.objects.get(pk=request.GET['carId'])
        if car is None:
            return ResponseMsg(False, None, '未知车辆')

        notes = dg_models.DeliveryNote.objects.filter(shop=shop, noteTime=timezone.now())
        if len(notes) == 0:
            note = dg_models.DeliveryNote.objects.create(shop=shop,
                noteTime=timezone.now(), createTime=timezone.now())
        elif len(notes) > 1:
            note = notes[0]
            for n in notes[1:]:
                n.delete()
        else:
            note = notes[0]

        goodsList = []
        totalPrice = 0
        for goodsItem in shop.goods.all():
            deliveriedGoods = note.goods.filter(goods__id=goodsItem.id)
            currentNumberDelivery = 0 if len(deliveriedGoods) == 0 else deliveriedGoods[0].actualDeliveryNumber
            carGoods = car.goods.filter(goods__id=goodsItem.goods.id)
            if len(carGoods) == 0:
                currentNumberInCar = 0
            else:
                currentNumberInCar = carGoods[0].carCurrentNumber

            totalPrice += currentNumberDelivery * goodsItem.price
            goodsList.append({
                'goodsItemId': goodsItem.id,
                'goodsId': goodsItem.goods.id,
                'name': goodsItem.goods.name,
                'currentNumberInCar': currentNumberInCar,
                'currentNumberDelivery': currentNumberDelivery,
                'targetNumber': goodsItem.targetNumber,
                'unitId': goodsItem.goods.unit.id,
                'unitName': goodsItem.goods.unit.name,
                'price': goodsItem.price,
            })


        noteInfo = {
            'shopId': shop.id,
            'carId': car.id,
            'noteId': note.id,
            'totalPrice': totalPrice,
            'actualPrice': note.actualPrice,
            'bookkeeping': note.bookkeeping,
            'goodsList': goodsList,
        }

        return ResponseMsg(True, noteInfo, None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, "异常")




"""
{
    'carId': 0,
    'shopId': 0,
    'noteId': 0,
    'actualPrice': 0,
    'bookkeeping': 0,
    'goodsList': [
        {
            'goodsItemId': 0,
            'goodsId': 0,
            'number': 0,
            'unitId': 0,
        },
    ]
}
"""
@login_required
def commitShopNote(request):
    try:
        if request.method == "POST":
            requestData = json.loads(request.body)
            car = dg_models.Car.objects.get(pk=requestData.get('carId'))
            if car is None:
                return ResponseMsg(False, None, "位置车辆")
            shop = dg_models.Shop.objects.get(pk=requestData.get('shopId'))
            if shop is None:
                return ResponseMsg(False, None, '未知商店')
            if requestData.get('noteId') is None:
                notes = dg_models.DeliveryNote.objects.filter(shop=shop, noteTime=timezone.now())
                if len( notes ) == 0:
                    note = dg_models.DeliveryNote.objects.get(pk=requestData.get('noteId'))
                else:
                    note = notes[0]
            else:
                note = dg_models.DeliveryNote.objects.get(pk=requestData.get('noteId'))
                if note is None:
                    note = dg_models.DeliveryNote.objects.create(shop=shop)
            noteGoodsInfo = {}
            # 计算本次所有的商品
            for goodsItem in ([] if requestData.get('goodsList') is None else requestData.get('goodsList')):
                deliveriedGoods = note.goods.filter(goods_id=goodsItem['goodsItemId'])
                shopGoods = shop.goods.get(pk=goodsItem['goodsItemId'])
                if shopGoods is None: continue
                noteGoodsInfo[goodsItem['goodsItemId']] = {
                    'goodsItemId': goodsItem['goodsItemId'],
                    'goodsId': goodsItem['goodsId'],
                    'number': goodsItem['number'],
                    'deliveriedNumber': 0 if len(deliveriedGoods) == 0 else deliveriedGoods[0].actualDeliveryNumber,
                    'unitId': goodsItem['unitId'],
                    'price': shopGoods.price,
                }
            # 计算以前添加的商品
            for goodsItem in note.goods.all():
                thisGoods = noteGoodsInfo.get(goodsItem.goods.id)
                if thisGoods is not None: continue
                shopGoods = shop.goods.get(pk=goodsItem.goods.id)
                if shopGoods is None: continue
                noteGoodsInfo[goodsItem.id] = {
                    'goodsItemId': goodsItem.goods.id,
                    'goodsId': goodsItem.goods.goods.id,
                    'number': 0,
                    'deliveriedNumber': goodsItem.actualDeliveryNumber,
                    'unitId': goodsItem.goods.unit.id,
                    'price': shopGoods.price,
                }
            note.goods.all().delete()
            # 更新订单
            totalPrice = 0
            for goodsItemId, goodsItem in noteGoodsInfo.items():
                # 更新车辆信息
                goods0 = car.goods.filter(goods_id=goodsItem['goodsId'])
                if len(goods0) != 0:
                    goods0.update(carCurrentNumber=F('carCurrentNumber') + goodsItem['deliveriedNumber'] - goodsItem['number'])
                # 更新商品
                if goodsItem['number'] > 0:
                    totalPrice += goodsItem['price'] * goodsItem['number']
                    shopGoods = shop.goods.get(pk=goodsItem['goodsItemId'])
                    if shopGoods is None: continue
                    note.goods.create(
                        goods=shopGoods,
                        actualDeliveryNumber=goodsItem['number']
                    )
            note.totalPrice = totalPrice
            note.actualPrice = requestData['actualPrice']
            note.bookkeeping = requestData['bookkeeping']
            note.save()
        return ResponseMsg(True, None, None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, '异常')
