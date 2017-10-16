# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .constant import INDUSTRY_LIST
from .constant import AREA_LIST

# Create your models here.


class StockBasicData(models.Model):
    """
    stock basic data
    """
    code = models.IntegerField(verbose_name=u'stock code', unique=True, db_index=True)
    name = models.CharField(verbose_name=u'stock name', max_length=20)
    c_name = models.SmallIntegerField(verbose_name=u'stock industry', choices=INDUSTRY_LIST)
    area = models.SmallIntegerField(verbose_name=u'area', choices=AREA_LIST)
