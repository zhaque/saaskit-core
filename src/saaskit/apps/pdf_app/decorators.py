# -*- encoding: utf-8 -*-
"""
Based on snippet from pisa's demo
look ad http://www.xhtml2pdf.com/
"""

from django.http import HttpResponse

import ho.pisa as pisa
#import cStringIO as StringIO

def pdf_response(func):
    def pdf_wrapper(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        pdf_context = pisa.pisaDocument(response.content)
        if not pdf_context.err:
            return HttpResponse(pdf_context.dest.getvalue(), mimetype='application/pdf')
        else:
            raise RuntimeError(pdfpdf_context.log)
    pdf_wrapper.__name__ = func.__name__
    return pdf_wrapper
