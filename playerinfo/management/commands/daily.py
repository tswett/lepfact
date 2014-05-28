import datetime

from django.core.management.base import BaseCommand
from playerinfo.models import Factory, Plot, WorkDoneDay

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

        for factory in Factory.objects.all():
            factory.upkeep()

        for plot in Plot.objects.all():
            plot.upkeep()

        WorkDoneDay(day=the_date).save()
