from rank_list.utils import get_last_charge_detail_by_inst
from rank_list.utils import get_last_ranklist_detail
from stock_classified.utils import get_last_stock_basic_info
from stock_classified.utils import get_realtime_stock_charge_info
import logging

logger = logging.getLogger("django.%s" % (__name__))


def get_last_charge_detail_by_inst_scheduled_job():
    """
    last charge detail by inst get daily
    :return:
    """
    get_last_charge_detail_by_inst()
    logger.info("done")


def get_last_ranklist_detail_scheduled_job():
    """
    last ranklist detail get daily
    :return:
    """
    get_last_ranklist_detail()
    logger.info("done")


def get_last_stock_basic_info_scheduled_job():
    """
    last stock info get daily (full)
    :return:
    """
    get_last_stock_basic_info()
    logger.info("done")


def get_realtime_stock_charge_info_scheduled_job():
    """
    real time stock charge info parse
    :return: 
    """
    code_list = ["000786", "300654", "000878", "603367", "000968", "300240", "000605", "300701"]
    get_realtime_stock_charge_info(code_list)
    logger.info("done")
