# -*- coding: utf-8 -*-

"""
ranklist utils
author: houjincheng@163.com
date: 2017-10-15
"""

from .models import RankListDailyData
from .models import RANK_REASON
import tushare as ts
import logging
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf8')  # gb2312,gbk

logging.basicConfig()
logger = logging.getLogger("django.%s" % (__name__))


def get_last_charge_detail_by_inst():
    """
    :return:
    """
    fields = ['code', 'name', 'date', 'bamount', 'samount', 'type']
    inst_detail = ts.inst_detail()
    inst_detail_len = len(inst_detail)
    if inst_detail_len == 0:
        logger.info("no data received")
        # todo: add email system

    bulk_list = []
    max_date = max(inst_detail['date'])
    if RankListDailyData.objects.filter(type_date=max_date).exists():
        return

    for i in range(inst_detail_len):
        per_dict = dict()
        for f in fields:
            per_dict.update({f:inst_detail[f][i]})
        if not per_dict.get('date'):
            continue
        if per_dict.get('date') != max_date:
            continue
        r_model = RankListDailyData(type_date=per_dict.get('date'), code=per_dict.get('code'),
                                    name=per_dict.get('name'),bamount=per_dict.get('bamount'),
                                    samount=per_dict.get('samount'),
                                    type=compare_by_value_get_key(RANK_REASON, per_dict.get('type')))
        bulk_list.append(r_model)
    RankListDailyData.objects.bulk_create(bulk_list)


def compare_by_value_get_key(item, content):
    """
    return key according to given content
    :param item: structure like [[0,0], [1, 0]]
    :param content: string
    :return:
    """
    # todo: exception define ultra
    # todo: code review
    for i in item:
        if i[1] == content:
            return i[0]
    logger.error("type not match, current type: %s" % content)
    return None

