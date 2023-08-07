import hashlib
import os
from pathlib import PurePath, PureWindowsPath, PurePosixPath

from django.contrib.auth.models import AbstractUser
from django.db import models

from application import dispatch
from apps.utils.models import CoreModel, table_prefix


class VipCard(CoreModel):
    """ 会员卡配置 """
    name = models.CharField(max_length=20, verbose_name='会员卡名称', blank=True, null=True, help_text='会员卡名称')
    # rebate = models.IntegerField(verbose_name='折扣', blank=True, null=True, default=0, help_text='折扣')
    vipType = models.CharField(max_length=20, verbose_name='VIP类型', null=True, blank=True, help_text='VIP类型')
    sort = models.IntegerField(verbose_name='排序', null=True, blank=True, help_text='排序')
    discount = models.IntegerField(verbose_name='折扣', null=True, blank=True, help_text='折扣', default=0)
    amount = models.DecimalField(max_length=10, verbose_name='购买金额', null=True, blank=True, help_text='购买金额',
                                 decimal_places=2,
                                 max_digits=5,
                                 default=0)
    isRecommend = models.IntegerField(verbose_name='是否推荐', null=True, blank=True, help_text='是否推荐', default=0)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "vip_card"
        verbose_name = "会员卡配置表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.name


class UserVipCard(CoreModel):
    """ 用户会员卡 """
    user = models.ForeignKey(to='admin.Users', verbose_name="关联用户",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="关联用户",
                             related_name='user_vip_card')
    vipCard = models.ForeignKey(to='VipCard', verbose_name="关联会员卡配置",
                                on_delete=models.PROTECT,
                                db_constraint=False,
                                null=True,
                                blank=True,
                                help_text="关联会员卡配置", )
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "user_vip_card"
        verbose_name = "用户会员卡"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.user.username


class UserAddr(CoreModel):
    """ 用户地址 """
    user = models.ForeignKey(to='admin.Users', verbose_name="关联用户",
                             on_delete=models.PROTECT,
                             db_constraint=False,
                             null=True,
                             blank=True,
                             help_text="关联用户",
                             related_name='user_addr')
    addr = models.CharField(max_length=100, verbose_name='用户地址', null=True, help_text='用户地址')
    isDefault = models.IntegerField(verbose_name='是否默认', null=True, blank=True, help_text='是否默认', default=1)
    status = models.IntegerField(verbose_name='状态', null=True, blank=True, help_text='状态', default=0)

    class Meta:
        db_table = table_prefix + "user_addr"
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.user.username
