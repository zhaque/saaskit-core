from datetime import datetime, timedelta
from django.conf import settings
from django.core import management
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
from saaskit.trans import run

class Command(LabelCommand):
  help = 'Translate all .po files using Google Translate.'
  args = 'available lang from setting.py or "all"'
  label = 'available lang from setting.py or "all"'

  ALL = 'all'

  def handle_label(self, label, **options):
    lang_exists = False
    for lang in settings.LANGUAGES:
      if label in lang:
        lang_exists = True
    if lang_exists or label==self.ALL:
      self.translate(label)
    else:
      print 'Language "%s" was not found in settings.py' % label

  def translate(self, lang):
    if lang == self.ALL:
      lang=None
    run(lang)
