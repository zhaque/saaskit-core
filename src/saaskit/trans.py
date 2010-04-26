from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rosetta.polib import pofile
from rosetta.poutil import find_pos, pagination_range
from rosetta.conf import settings as rosetta_settings
import re, os, rosetta, datetime, unicodedata
from gt import translate

def fix_nls(in_,out_):
    """Fixes submitted translations by filtering carriage returns and pairing
    newlines at the begging and end of the translated string with the original
    """
    if 0 == len(in_) or 0 == len(out_):
        return out_

    if "\r" in out_ and "\r" not in in_:
        out_=out_.replace("\r",'')

    if "\n" == in_[0] and "\n" != out_[0]:
        out_ = "\n" + out_
    elif "\n" != in_[0] and "\n" == out_[0]:
        out_ = out_.lstrip()
    if "\n" == in_[-1] and "\n" != out_[-1]:
        out_ = out_ + "\n"
    elif "\n" != in_[-1] and "\n" == out_[-1]:
        out_ = out_.rstrip()
    return out_

def get_app_name(path):
    app = path.split("/locale")[0].split("/")[-1]
    return app

def list_languages():
    languages = []
    has_pos = False
    for language in settings.LANGUAGES:
        pos = find_pos(language[0])        
        has_pos = has_pos or len(pos)
        languages.append(
            (language[0], 
            language[1],
            [(get_app_name(l), os.path.realpath(l), pofile(l)) for l in  pos],
            )
        )
    return languages

def run():
  languages = list_languages()
  for lang, lang_name, po in languages:
    for app, path, po_file in po:
      messages = po_file.untranslated_entries()
      print 'Language: %s, app: %s, untranslated: %d' % (lang_name, app, len(messages))
      for msg in messages:
        try:
#          print '%s to %s' % (msg.msgid, lang)
          msg.msgstr = fix_nls(msg.msgid, translate(msg.msgid, to=lang))
#          print msg.msgstr
        except TypeError:
          pass
        except IOError:
          pass
      po_file.save()
      po_file.save_as_mofile(path.replace('.po','.mo'))

