# -*- coding: UTF-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User


#用户
class User(AbstractUser):
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


# 单位类型
class UnitCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='单位类型')

    class Meta:
        verbose_name = '单位类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 单位
class Unit(models.Model):
    name = models.CharField(max_length=64, verbose_name='名称')
    category = models.ForeignKey(UnitCategory, on_delete=models.CASCADE, verbose_name='类型')
    isBase = models.BooleanField(default=False, verbose_name="是否是基础单位")
    ratio = models.FloatField(default=1, verbose_name='换算比率')


    class Meta:
        verbose_name = '单位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品分类
class GoodsCategory(models.Model):
    name = models.CharField(max_length=64, verbose_name='商品分类')
    index = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name


# 商品
class Goods(models.Model):
    name = models.CharField(max_length=128, verbose_name='商品名称')
    category = models.ForeignKey(GoodsCategory, on_delete=models.SET_NULL, null=True, verbose_name='商品类型')
    price = models.FloatField(verbose_name='价格')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, verbose_name='单位')
    image_url_i = models.ImageField(upload_to='product/%Y/%m', default='product/default.jpg', verbose_name='展示图片路径')
    index = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['index', ]

    def __str__(self):
        return self.name


# 商家-商品
class GoodsItem(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    price = models.FloatField(verbose_name='价格')
    # unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, verbose_name='单位')
    currentNumber = models.IntegerField(default=0, verbose_name='当前数量')
    # currentNumberUnit = models.ForeignKey(Unit, related_name='currentNumberUnit', on_delete=models.SET_NULL, null=True, verbose_name='当前数量单位')
    targetNumber = models.IntegerField(default=0, verbose_name='目标数量')
    # targetNumberUnit = models.ForeignKey(Unit, related_name='targetNumberUnit', on_delete=models.SET_NULL, null=True, verbose_name='目标数量单位')
    deliveryNumber = models.IntegerField(default=0, verbose_name='送货数量')
    # deliveryNumberUnit = models.ForeignKey(Unit, related_name='deliveryNumberUnit', on_delete=models.SET_NULL, null=True, verbose_name='送货数量单位')

    class Meta:
        verbose_name = '商家-商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}({}/{})'.format(self.goods.name, self.price, self.goods.unit.name)


# 仓库
class Warehouse(models.Model):
    name = models.CharField(max_length=128, verbose_name='仓库名称')
    goods = models.ManyToManyField(GoodsItem, blank=True, verbose_name='商品')
    index = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        verbose_name = '仓库'
        verbose_name_plural = verbose_name
        ordering = ['index', ]

    def __str__(self):
        return self.name


# 商家
class Shop(models.Model):
    name = models.CharField(max_length=128, verbose_name='商家名称')
    goods = models.ManyToManyField(GoodsItem, blank=True, verbose_name='商品')
    longitude = models.FloatField(verbose_name='经度')
    latitude = models.FloatField(verbose_name='纬度')
    scope = models.FloatField(default=100, verbose_name='范围(米)')
    index = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        verbose_name = '商家'
        verbose_name_plural = verbose_name
        ordering = ['index', ]

    def __str__(self):
        return self.name


# 送货单-货物
class DeliveryNoteGoods(models.Model):
    goods = models.ForeignKey(GoodsItem, on_delete=models.CASCADE, verbose_name='商品')
    actualDeliveryNumber = models.IntegerField(default=0, verbose_name='送货数量')
    # actualDeliveryNumberUnit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, verbose_name='送货数量单位')

    class Meta:
        verbose_name = '送货单-货物'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}--卸载{}{}--{}/{}'.format(self.goods.goods.name, self.actualDeliveryNumber, self.goods.goods.unit.name, self.goods.price, self.goods.goods.unit.name)


# 送货单
class DeliveryNote(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='商家')
    goods = models.ManyToManyField(DeliveryNoteGoods, blank=True, verbose_name='货物')
    totalPrice = models.FloatField(default=0, verbose_name='总金额')
    actualPrice = models.FloatField(default=0, verbose_name='实收金额')
    bookkeeping = models.FloatField(default=0, verbose_name='记账金额')
    status = models.IntegerField(default=0, verbose_name='状态', help_text='0:未完成 1:已完成')
    noteTime = models.DateField(null=False, verbose_name='订单日期')
    finishTime = models.DateTimeField(null=True, verbose_name='完成日期')
    createTime = models.DateTimeField(auto_created=True)
    updateTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '送货单'
        verbose_name_plural = verbose_name
        unique_together = ('shop', 'noteTime')
        ordering = ['-noteTime']

    def __str__(self):
        return self.shop.name + '---' + self.noteTime.strftime('%Y-%m-%d %H:%I:%S')


# 货运路线
class Route(models.Model):
    name = models.CharField(max_length=128, verbose_name='路线名称')
    shops = models.ManyToManyField(Shop, blank=True, verbose_name='商家')
    index = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        verbose_name = '路线'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name


# 车辆-商品
class CarGoodsItem(models.Model):
    carName = models.CharField(max_length=128, verbose_name='车辆')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    carCurrentNumber = models.IntegerField(default=0, verbose_name='当前数量')
    # carCurrentNumberUnit = models.ForeignKey(Unit, related_name='carCurrentNumberUnit', on_delete=models.SET_NULL, null=True, verbose_name='当前数量单位')
    carTargetNumber = models.IntegerField(default=0, verbose_name='目标数量')
    # carTargetNumberUnit = models.ForeignKey(Unit, related_name='carTargetNumberUnit', on_delete=models.SET_NULL, null=True, verbose_name='目标数量单位')

    class Meta:
        verbose_name = '车辆-商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}-{}'.format(self.carName, self.goods.name)

# 货运车
class Car(models.Model):
    name = models.CharField(max_length=128, verbose_name='车')
    driver = models.ForeignKey(User, related_name='driver', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='司机')
    passenger = models.ManyToManyField(User, related_name='passenger', blank=True, verbose_name='随车人员')
    route = models.OneToOneField(Route, on_delete=models.DO_NOTHING, verbose_name='路线')
    goods = models.ManyToManyField(CarGoodsItem, blank=True, verbose_name='商品')
    index = models.IntegerField(default=1, verbose_name='排序')

    class Meta:
        verbose_name = '货车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name