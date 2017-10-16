# -*- coding:utf-8 -*-
"""
# @Author  : houjincheng1992@163.com
# @Time    : 17/10/16 下午4:31
# @File    : utils.py
"""
from .models import StockBasicData
from rank_list.utils import compare_by_value_get_key
from .constant import INDUSTRY_LIST
from .constant import AREA_LIST
import tushare as ts
import logging

logger = logging.getLogger("django.%s" % (__name__))


def get_last_stock_basic_info():
    """
    get last stock info (full): include code name classify and area
    :return: 
    """
    industry_field = ["code", "name", "c_name"]
    area_field = ["area"]

    industry_classify = ts.get_industry_classified()
    area_classify = ts.get_area_classified()

    tmp_dict = dict()
    code_list = []
    for i in range(len(industry_classify)):
        cur_code = industry_classify['code'][i]
        for f in industry_field:
            if cur_code not in tmp_dict:
                tmp_dict[cur_code] = {}
            tmp_dict[cur_code].update({f: industry_classify[f][i]})
        code_list.append(int(cur_code))
    for i in range(len(area_classify)):
        cur_code = area_classify['code'][i]
        for f in area_field:
            if cur_code in tmp_dict:
                # tmp_dict[cur_code] = {}
                tmp_dict[cur_code].update({f: area_classify[f][i]})
        # code_list.append(cur_code)

    stock_contain = list(StockBasicData.objects.filter(code__in=code_list).
                         values_list("code", flat=True))
    uncontain_list = set(code_list) - set(stock_contain)
    logger.debug("uncontain_list: %s" % uncontain_list)

    bulk_list = []
    for uncontain in uncontain_list:
        per_dict = tmp_dict[str(uncontain).zfill(6)]
        if per_dict.get("code") and per_dict.get("name") and per_dict.get("c_name") and per_dict.get("area"):
            if uncontain != per_dict.get("code"):
                logger.info("not equal %s, %s" % (uncontain, per_dict.get("code")))
            r_model = StockBasicData(code=per_dict.get("code"), name=per_dict.get("name"),
                                     c_name=compare_by_value_get_key(INDUSTRY_LIST, per_dict.get("c_name")), area=compare_by_value_get_key(AREA_LIST, per_dict.get("area")))
            logger.info("%s, %s, %s, %s" % (per_dict.get("code"), per_dict.get("name"), per_dict.get("c_name"), per_dict.get("area")))
            bulk_list.append(r_model)
    StockBasicData.objects.bulk_create(bulk_list)

