import logging
import json

from django.http import response
from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.db import models

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
                    'id': goodsItem.id,
                    'goods_id': goodsItem.goods.id,
                    'name': goodsItem.goods.name,
                    'currentNumber': goodsItem.currentNumber,
                    'unit_id': goodsItem.currentNumberUnit.id,
                    'unit_name': goodsItem.currentNumberUnit.name,
                } for goodsItem in car.goods.all()
            ]
        }

        return ResponseMsg(True, carInfo, None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, '异常')


@login_required
def getShopGoodsList(request):
    try:
        shop = dg_models.Shop.objects.get(pk=request.GET['shopId'])
        if shop is None:
            return ResponseMsg(False, None, '未知商家！')
        goodsList = []
        for goodsItem in shop.goods.all():
            goodsList.append({
                'id': goodsItem.id,
                'goods_id': goodsItem.goods.id,
                'name': goodsItem.goods.name,
                'currentNumber': goodsItem.currentNumber,
                'currentNumberUnit_id': goodsItem.currentNumberUnit.id,
                'currentNumberUnit_name': goodsItem.currentNumberUnit.name,
                'targetNumber': goodsItem.targetNumber,
                'targetNumberUnit_id': goodsItem.targetNumberUnit.id,
                'targetNumberUnit_name': goodsItem.targetNumberUnit.name,
            })

        return ResponseMsg(True, goodsList, None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, '异常')

