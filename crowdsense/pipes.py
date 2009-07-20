from django.utils.safestring import SafeUnicode

import django_pipes

class TwitterSearch(django_pipes.Pipe):
    uri = "http://search.twitter.com/search.json"
    parameters = { 'q' : None,
                   'lang' : None,
                   'rpp' : None,
                   'since_id' : None,
                   'geocode' : None
                   }
    name = 'Twitter Search'
    cache_expiry = 15

    def render(self):
        rv = ['<ul>']
        for result in self.results:
            rv.append(u'<li lang="%s"><img src="%s">%s: %s</li>' % (
                result.iso_language_code,
                result.profile_image_url,
                result.from_user,
                result.text ) )
        rv.append('</ul>')
        return SafeUnicode(u''.join(rv))

class GoogleSearch(django_pipes.Pipe):
    uri = "http://ajax.googleapis.com/ajax/services/search/web"
    parameters = { 'q' : None,
                   }
    name = 'Google Search'
