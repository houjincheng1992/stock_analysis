from rank_list.utils import get_last_charge_detail_by_inst
from rank_list.utils import get_last_ranklist_detail
import logging

logger = logging.getLogger("django.%s" % (__name__))


def get_last_charge_detail_by_inst_scheduled_job():
    get_last_charge_detail_by_inst()
    logger.info("done")


def get_last_ranklist_detail_scheduled_job():
    get_last_ranklist_detail()
    logger.info("done")