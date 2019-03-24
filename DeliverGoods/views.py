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

from DeliverGoods import models as dg_models


logger = logging.getLogger('DeliverGoods.views')


class ResponseMsg(response.JsonResponse):
    def __init__(self, status, result=None, msg=None):
        if isinstance(result, QuerySet):
            result = json.loads(serializers.serialize('json', result, cls=DjangoJSONEncoder))
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
def getRouteShopList(request):
    try:
        car_list = dg_models.Car.objects.filter(driver=request.user.id)
        if car_list is None or len(car_list) == 0:
            return ResponseMsg(False, None, '你不是司机')
        if len(car_list) > 1:
            return ResponseMsg(False, None, '你有多个路线，请联系系统管理员')
        car = car_list[0]
        if car.route is None:
            return ResponseMsg(False, None, '没有可用路线,请联系系统管理员')
        return ResponseMsg(True, car.route.shops.all(), None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, '异常')


@login_required
def getShopGoodsList(request):
    try:
        shop = dg_models.Shop.objects.get(pk=shopId)
        if shop is None:
            return ResponseMsg(False, None, '未知商家！')
        return ResponseMsg(True, shop.goods.all(), None)
    except Exception as ee:
        logger.error(ee)
        return ResponseMsg(False, None, '异常')
