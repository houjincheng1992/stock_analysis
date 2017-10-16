# -*- coding: utf-8 -*-

"""
ranklist model
author: houjincheng@163.com
date: 2017-10-15
"""

from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.

RANK_REASON = (
    (0, u'连续三个交易日内，日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20%的股票'),
    (1, u'连续三个交易日内，涨幅偏离值累计达20%的证券'),
    (2, u'涨幅偏离值达7%的证券'),
    (3, u'无价格涨跌幅限制的证券'),
    (4, u'换手率达20%的证券'),
    (5, u'跌幅偏离值达7%的证券'),
)


class InstChargeDailyData(models.Model):
    """
    Institute charge daily data in db
    """
    type_date = models.DateField(verbose_name=u'type in date', default=datetime.date.today, db_index=True)
    code = models.IntegerField(verbose_name=u'stock code', db_index=True)
    name = models.CharField(verbose_name=u'stock name', max_length=20)
    bamount = models.IntegerField(verbose_name=u'buy amount')
    samount = models.IntegerField(verbose_name=u'sold amount')
    type = models.SmallIntegerField(verbose_name=u'describe in ranklist', choices=RANK_REASON)

    class Meta(object):
        """
        meta
        """
        unique_together = ['code', 'type_date', 'type']