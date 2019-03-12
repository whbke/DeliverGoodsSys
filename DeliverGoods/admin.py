from django.contrib import admin

# Register your models here.

from DeliverGoods.models import User, UnitCategory, Unit, GoodsCategory,\
    Goods, Warehouse, Shop, ShopGoodsItem, DeliveryNote, DeliveryNoteGoods,\
    Route, Car

# Register your models here.
admin.site.register([User, UnitCategory, Unit, GoodsCategory,
    Goods, ShopGoodsItem, DeliveryNoteGoods])


class ShopAdmin(admin.ModelAdmin):
    filter_horizontal = ['goods']
admin.site.register(Shop, ShopAdmin)


class WarehouseAdmin(admin.ModelAdmin):
    filter_horizontal = ['goods']
admin.site.register(Warehouse, WarehouseAdmin)


class DeliveryNoteAdmin(admin.ModelAdmin):
    filter_horizontal = ['goods']
admin.site.register(DeliveryNote, DeliveryNoteAdmin)


class RouteAdmin(admin.ModelAdmin):
    filter_horizontal = ['shops']
admin.site.register(Route, RouteAdmin)


class CarAdmin(admin.ModelAdmin):
    filter_horizontal = ['passenger']
admin.site.register(Car, CarAdmin)