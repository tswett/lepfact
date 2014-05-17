import datetime

from django.core.management.base import BaseCommand
from playerinfo.models import WorkDoneDay

class Command(BaseCommand):
    args = '[timestamp]'
    help = 'Runs daily tasks for timestamp (a Unix timestamp), defaulting to today.  Does nothing if daily tasks have already been done for that day.'

    def handle(self, *args, **options):
        if args:
            the_date = datetime.date.fromtimestamp(int(args[0]))
        else:
            the_date = datetime.date.today()

        if WorkDoneDay.objects.filter(day=the_date):
            self.stdout.write('Daily tasks have already been run for %s; exiting.' % the_date.strftime('%d %b %Y'))
            return

        self.stdout.write('Running daily tasks for %s.' % the_date.strftime('%d %b %Y'))

        WorkDoneDay(day=the_date).save()
