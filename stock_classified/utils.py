# -*- coding:utf-8 -*-
"""
# @Author  : houjincheng1992@163.com
# @Time    : 17/10/16 下午4:31
# @File    : utils.py
"""
from .models import StockBasicData
from .models import StockChargeRealTimeData
from rank_list.utils import compare_by_value_get_key
from .constant import INDUSTRY_LIST
from .constant import AREA_LIST
import tushare as ts
import datetime
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
        if per_dict.get("code") and per_dict.get("name") and per_dict.get("c_name") and \
                per_dict.get("area"):
            if uncontain != per_dict.get("code"):
                logger.info("not equal %s, %s" % (uncontain, per_dict.get("code")))
            r_model = StockBasicData(code=per_dict.get("code"), name=per_dict.get("name"),
                                     c_name=compare_by_value_get_key(INDUSTRY_LIST,
                                                                     per_dict.get("c_name")),
                                     area=compare_by_value_get_key(AREA_LIST, per_dict.get("area")))
            logger.info("%s, %s, %s, %s" % (per_dict.get("code"), per_dict.get("name"),
                                            per_dict.get("c_name"), per_dict.get("area")))
            bulk_list.append(r_model)
    StockBasicData.objects.bulk_create(bulk_list)


def get_realtime_stock_charge_info(stock_list):
    """
    get realtime stock charge info
    :return:
    """
    try:
        field = ['code', 'name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume',
                 'amount', 'date', 'time']
        json_field = [['b1_v', 'b1_p'], ['b2_v', 'b2_p'], ['b3_v', 'b3_p'], ['b4_v', 'b4_p'],
                      ['b5_v', 'b5_p'], ['a1_v', 'a1_p'], ['a2_v', 'a2_p'], ['a3_v', 'a3_p'],
                      ['a4_v', 'a4_p'], ['a5_v', 'a5_p']]
        interest_list = []
        if isinstance(stock_list, list):
            interest_list = stock_list
        df = ts.get_realtime_quotes(interest_list)

        tmp_dict = dict()
        for i in range(len(df)):
            cur_code = df['code'][i]
            for f in field:
                if cur_code not in tmp_dict:
                    tmp_dict[cur_code] = {}
                tmp_dict[cur_code].update({f: df[f][i]})
            type_datetime = datetime.datetime.strptime(df['date'][i] + " " + df['time'][i],
                                                       '%Y-%m-%d %H:%M:%S')
            tmp_dict[cur_code].update({'type_datetime': type_datetime})

            json_dict = dict()
            for f in json_field:
                json_dict.update({f[0]: df[f[0]][i], f[1]: df[f[1]][i]})
            tmp_dict[cur_code].update({"bavp": json_dict})

        bulk_list = []
        for key in tmp_dict.keys():
            cur_stock = StockChargeRealTimeData.objects.update_or_create(
                code=key,
                type_datetime=tmp_dict[key]['type_datetime'],
                defaults={"name": tmp_dict[key]['name'], "open": tmp_dict[key]['open'],
                          "pre_close": tmp_dict[key]['pre_close'], "price": tmp_dict[key]['price'],
                          "high": tmp_dict[key]['high'], "low": tmp_dict[key]['low'],
                          "bid": tmp_dict[key]['bid'], "ask": tmp_dict[key]['ask'],
                          "volume": tmp_dict[key]['volume'], "bavp": tmp_dict[key]['bavp']}
            )

        #     bulk_list.append(cur_stock)
        # StockChargeRealTimeData.objects.bulk_create(bulk_list)
    except Exception as e:
        logger.warning("%s" % e)







