from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # inital encoding ut this later on lead to issues with the generating pdf files
    # pdf_encoding = "ISO-8859-1"
    pdf_encoding = "UTF-8"
    pdf = pisa.pisaDocument(BytesIO(html.encode(pdf_encoding)), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
