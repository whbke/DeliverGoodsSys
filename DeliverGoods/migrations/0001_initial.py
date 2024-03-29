# Generated by Django 2.1.7 on 2019-04-03 15:39

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='车')),
                ('index', models.IntegerField(default=1, verbose_name='排序')),
            ],
            options={
                'verbose_name': '货车',
                'verbose_name_plural': '货车',
            },
        ),
        migrations.CreateModel(
            name='CarGoodsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carName', models.CharField(max_length=128, verbose_name='车辆')),
                ('carCurrentNumber', models.IntegerField(default=0, verbose_name='当前数量')),
                ('carTargetNumber', models.IntegerField(default=0, verbose_name='目标数量')),
            ],
            options={
                'verbose_name': '车辆-商品',
                'verbose_name_plural': '车辆-商品',
            },
        ),
        migrations.CreateModel(
            name='DeliveryNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateTimeField(auto_created=True)),
                ('totalPrice', models.FloatField(default=0, verbose_name='总金额')),
                ('actualPrice', models.FloatField(default=0, verbose_name='实收金额')),
                ('bookkeeping', models.FloatField(default=0, verbose_name='记账金额')),
                ('status', models.IntegerField(default=0, help_text='0:未完成 1:已完成', verbose_name='状态')),
                ('noteTime', models.DateField(verbose_name='订单日期')),
                ('finishTime', models.DateTimeField(null=True, verbose_name='完成日期')),
                ('updateTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '送货单',
                'verbose_name_plural': '送货单',
                'ordering': ['-noteTime'],
            },
        ),
        migrations.CreateModel(
            name='DeliveryNoteGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actualDeliveryNumber', models.IntegerField(default=0, verbose_name='送货数量')),
            ],
            options={
                'verbose_name': '送货单-货物',
                'verbose_name_plural': '送货单-货物',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='商品名称')),
                ('price', models.FloatField(verbose_name='价格')),
                ('image_url_i', models.ImageField(default='product/default.jpg', upload_to='product/%Y/%m', verbose_name='展示图片路径')),
                ('index', models.IntegerField(default=1, verbose_name='排序')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='商品分类')),
                ('index', models.IntegerField(default=1, verbose_name='排序')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='GoodsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='价格')),
                ('currentNumber', models.IntegerField(default=0, verbose_name='当前数量')),
                ('targetNumber', models.IntegerField(default=0, verbose_name='目标数量')),
                ('deliveryNumber', models.IntegerField(default=0, verbose_name='送货数量')),
            ],
            options={
                'verbose_name': '商家-商品',
                'verbose_name_plural': '商家-商品',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='路线名称')),
                ('index', models.IntegerField(default=1, verbose_name='排序')),
            ],
            options={
                'verbose_name': '路线',
                'verbose_name_plural': '路线',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='商家名称')),
                ('longitude', models.FloatField(verbose_name='经度')),
                ('latitude', models.FloatField(verbose_name='纬度')),
                ('scope', models.FloatField(default=100, verbose_name='范围(米)')),
                ('index', models.IntegerField(default=1, verbose_name='排序')),
                ('goods', models.ManyToManyField(blank=True, to='DeliverGoods.GoodsItem', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商家',
                'verbose_name_plural': '商家',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('isBase', models.BooleanField(default=False, verbose_name='是否是基础单位')),
                ('ratio', models.FloatField(default=1, verbose_name='换算比率')),
            ],
            options={
                'verbose_name': '单位',
                'verbose_name_plural': '单位',
            },
        ),
        migrations.CreateModel(
            name='UnitCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='单位类型')),
            ],
            options={
                'verbose_name': '单位类型',
                'verbose_name_plural': '单位类型',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='仓库名称')),
                ('index', models.IntegerField(default=1, verbose_name='排序')),
                ('goods', models.ManyToManyField(blank=True, to='DeliverGoods.GoodsItem', verbose_name='商品')),
            ],
            options={
                'verbose_name': '仓库',
                'verbose_name_plural': '仓库',
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('qq', models.CharField(blank=True, max_length=20, null=True, verbose_name='QQ号码')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='unit',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DeliverGoods.UnitCategory', verbose_name='类型'),
        ),
        migrations.AddField(
            model_name='route',
            name='shops',
            field=models.ManyToManyField(blank=True, to='DeliverGoods.Shop', verbose_name='商家'),
        ),
        migrations.AddField(
            model_name='goodsitem',
            name='currentNumberUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currentNumberUnit', to='DeliverGoods.Unit', verbose_name='当前数量单位'),
        ),
        migrations.AddField(
            model_name='goodsitem',
            name='deliveryNumberUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deliveryNumberUnit', to='DeliverGoods.Unit', verbose_name='送货数量单位'),
        ),
        migrations.AddField(
            model_name='goodsitem',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DeliverGoods.Goods', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='goodsitem',
            name='targetNumberUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='targetNumberUnit', to='DeliverGoods.Unit', verbose_name='目标数量单位'),
        ),
        migrations.AddField(
            model_name='goodsitem',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DeliverGoods.Unit', verbose_name='单位'),
        ),
        migrations.AddField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DeliverGoods.GoodsCategory', verbose_name='商品类型'),
        ),
        migrations.AddField(
            model_name='goods',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DeliverGoods.Unit', verbose_name='单位'),
        ),
        migrations.AddField(
            model_name='deliverynotegoods',
            name='actualDeliveryNumberUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DeliverGoods.Unit', verbose_name='送货数量单位'),
        ),
        migrations.AddField(
            model_name='deliverynotegoods',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DeliverGoods.GoodsItem', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='goods',
            field=models.ManyToManyField(blank=True, to='DeliverGoods.DeliveryNoteGoods', verbose_name='货物'),
        ),
        migrations.AddField(
            model_name='deliverynote',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DeliverGoods.Shop', verbose_name='商家'),
        ),
        migrations.AddField(
            model_name='cargoodsitem',
            name='carCurrentNumberUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carCurrentNumberUnit', to='DeliverGoods.Unit', verbose_name='当前数量单位'),
        ),
        migrations.AddField(
            model_name='cargoodsitem',
            name='carTargetNumberUnit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carTargetNumberUnit', to='DeliverGoods.Unit', verbose_name='目标数量单位'),
        ),
        migrations.AddField(
            model_name='cargoodsitem',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DeliverGoods.Goods', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='car',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver', to=settings.AUTH_USER_MODEL, verbose_name='司机'),
        ),
        migrations.AddField(
            model_name='car',
            name='goods',
            field=models.ManyToManyField(blank=True, to='DeliverGoods.CarGoodsItem', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='car',
            name='passenger',
            field=models.ManyToManyField(blank=True, related_name='passenger', to=settings.AUTH_USER_MODEL, verbose_name='随车人员'),
        ),
        migrations.AddField(
            model_name='car',
            name='route',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='DeliverGoods.Route', verbose_name='路线'),
        ),
        migrations.AlterUniqueTogether(
            name='deliverynote',
            unique_together={('shop', 'noteTime')},
        ),
    ]
