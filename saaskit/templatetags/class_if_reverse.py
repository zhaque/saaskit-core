from django import template
from django.core.urlresolvers import reverse

register = template.Library()

class ClassIfReverseNode(template.Node):
    def __init__(self, url_path, class_name):
        self.class_name = class_name
        self.url_path = url_path
    def render(self, context):
        if context['request'].path.startswith(self.url_path):
            return ' class="%s"' % self.class_name
        else: return ''

def do_class_if_reverse(parser, token):
    try: tag_name, url, cls = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments: url, css class" % token.contents.split()[0]
    if not url.startswith('/'): url = reverse(url)
    return ClassIfReverseNode(url, cls)

register.tag('class_if_reverse', do_class_if_reverse)
