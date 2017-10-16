# -*- coding:utf-8 -*-
"""
# @Author  : houjincheng1992@163.com
# @Time    : 17/10/16 下午4:31
# @File    : utils.py
"""
from .models import StockBasicData
import tushare as ts


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
        code_list.append(cur_code)
    for i in range(len(area_field)):
        cur_code = area_classify['code'][i]
        for f in industry_field:
            if cur_code not in tmp_dict:
                tmp_dict[cur_code] = {}
            tmp_dict[cur_code].update({f: area_classify[f][i]})
        code_list.append(cur_code)

    stock_contain = list(StockBasicData.objects.filter(code__in=code_list).
                         values_list("code", flat=True))
    uncontain_list = set(code_list) - set(stock_contain)

    bulk_list = []
    for uncontain in uncontain_list:
        per_dict = tmp_dict[uncontain]
        r_model = StockBasicData(code=per_dict.get("code"), name=per_dict.get("name"),
                                 c_name=per_dict.get("c_name"), area=per_dict.get("area"))
        bulk_list.append(r_model)
    StockBasicData.objects.bulk_create(bulk_list)

