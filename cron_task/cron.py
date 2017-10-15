from rank_list.utils import get_last_charge_detail_by_inst
import logging

logger = logging.getLogger("django.%s" % (__name__))


def get_last_charge_detail_by_inst_scheduled_job():
    get_last_charge_detail_by_inst()
    logger.info("done")
