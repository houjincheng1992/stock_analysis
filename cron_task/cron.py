from rank_list.utils import get_last_charge_detail_by_inst
from rank_list.utils import get_last_ranklist_detail
from stock_classified.utils import get_last_stock_basic_info
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
