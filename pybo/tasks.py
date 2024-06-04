
import logging

from django.config.settings import prod

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)


def load430():
    for card in PreCard.objects.filter(moving_date__date=timezone.now().date(), time="8, 9교시"):
        PreCard.objects.create(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)

def load620():
    for card in PreCard.objects.filter(moving_date__date=timezone.now().date(), time="1차야자"):
        PreCard.objects.create(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)

def mstatu():
    students = Student.objects.all()
    for student in students:
        Card.objects.create(to='재실', why='초기상태', stu=student, moving_date=timezone.now())

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BackgroundScheduler(timezone=TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      mstatu,
      trigger=CronTrigger(hour=“17”, minute = “25”),
      id="reset_card",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    logger.info("Added job 'reset_card'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")