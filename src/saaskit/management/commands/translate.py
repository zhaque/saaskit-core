from datetime import datetime, timedelta
from django.conf import settings
from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import NoArgsCommand
from saaskit.trans import run

class Command(NoArgsCommand):
  help = 'Translate all .po files using Google Translate.'
  def handle_noargs(self, **options):
      self.translate()

  def translate(self):
    run()
