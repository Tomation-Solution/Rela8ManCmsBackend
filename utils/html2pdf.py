from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    # Load the template with the provided context
    template = get_template(template_src)
    html = template.render(context_dict)

    # Create a BytesIO stream to write the PDF result into
    result = BytesIO()

    # Specify the encoding for the HTML content (UTF-8 is generally good for compatibility)
    pdf_encoding = "UTF-8"

    # Generate PDF from HTML
    pdf = pisa.pisaDocument(BytesIO(html.encode(pdf_encoding)), result)

    # Check if the PDF was generated successfully
    if not pdf.err:
        # Return the PDF as an HTTP response with proper content type
        return HttpResponse(result.getvalue(), content_type="application/pdf")

    # Return None if there was an error generating the PDF
    return None
