"""Scheduler using APScheduller
1 - Test scheduler Job - 5 sec after sanic start
2 - Clean /tmp folder - every 30 mins
"""
import os
import sys
import time
import shutil
from datetime import timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from loguru import logger
import backend.model as ax_model
import backend.misc as ax_misc

this = sys.modules[__name__]
scheduler = None


async def prn_job(message):
    """ Executed aftrer sanic app start to know if scheduler is working"""
    print(str(message))
    return False


async def clear_tmp_files():
    """ Delete all files from /tmp folder wich is expired """
    tmp_folder = ax_misc.path('tmp')
    for root, dirs, _ in os.walk(tmp_folder):
        del root
        for dir_name in dirs:
            dir_to_check = os.path.join(tmp_folder, dir_name)
            seconds = time.time() - os.path.getmtime(dir_to_check)
            minutes = int(seconds) / 60
            if minutes > 120:   # 120 minutes expiration time
                shutil.rmtree(dir_to_check)


def init_scheduler():
    """Initiate scheduller"""
    # https://apscheduler.readthedocs.io/en/latest/modules/schedulers/base.html#apscheduler.schedulers.base.BaseScheduler.add_job

    # TODO UTC must match timezone from config
    try:
        jobstores = {
            'default': SQLAlchemyJobStore(
                engine=ax_model.engine,
                tablename='_ax_scheduler_jobs'
            )
        }

        executors = {
            'default': AsyncIOExecutor()
        }

        this.scheduler = AsyncIOScheduler(
            jobstores=jobstores,
            executors=executors,
            timezone=ax_misc.timezone)
        this.scheduler.start()

        # this.scheduler.remove_all_jobs()
        # dt = datetime.now() + timedelta(seconds=5)
        moscow_dt = ax_misc.date() + timedelta(seconds=5)
        this.scheduler.add_job(
            prn_job,
            'date',
            run_date=moscow_dt,
            args=['SCHEDULER WORKS'],
            id='prn_job'
        )

        # Job cleaning /uploads/tmp folder. deletes files that are expired
        this.scheduler.add_job(clear_tmp_files, trigger='cron', minute='30')

    except Exception:
        logger.exception('Error initiating scheduler module. ')
        raise
