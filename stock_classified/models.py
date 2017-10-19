# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .constant import INDUSTRY_LIST
from .constant import AREA_LIST
import datetime

# Create your models here.


class StockBasicData(models.Model):
    """
    stock basic data
    """
    code = models.IntegerField(verbose_name=u'stock code', unique=True, db_index=True)
    name = models.CharField(verbose_name=u'stock name', max_length=20)
    c_name = models.SmallIntegerField(verbose_name=u'stock industry', choices=INDUSTRY_LIST, db_index=True)
    area = models.SmallIntegerField(verbose_name=u'area', choices=AREA_LIST, db_index=True)


class StockChargeRealTimeData(models.Model):
    """
    real time stock charge data
    """
    code = models.IntegerField(verbose_name=u'stock code', db_index=True)
    name = models.CharField(verbose_name=u'stock name', max_length=20)
    open = models.FloatField(verbose_name=u'open price', null=True)
    pre_close = models.FloatField(verbose_name=u'pre close price', null=True)
    price = models.FloatField(verbose_name=u'current price', null=True)
    high = models.FloatField(verbose_name=u'today max price', null=True)
    low = models.FloatField(verbose_name=u'today min price', null=True)
    bid = models.FloatField(verbose_name=u'buy 1 price', null=True)
    ask = models.FloatField(verbose_name=u'sold 1 price', null=True)
    volume = models.FloatField(verbose_name=u'bargin num', null=True)
    amount = models.FloatField(verbose_name=u'bargin price (yuan)', null=True)
    bavp = models.CharField(verbose_name=u'real time buy/sold bargin', max_length=200, null=True,
                            blank=True)
    type_datetime = models.DateTimeField(verbose_name=u'type in datetime',
                                         default=datetime.datetime.now(),
                                         db_index=True)

    class Meta(object):
        """
        meta
        """
        unique_together = ["code", "type_datetime"]
