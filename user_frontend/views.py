from codecs import decode
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string

from orders.models import Order, OrderProduct
from store.models import Product, ProductImage, ReviewRating


from weasyprint import HTML
import tempfile

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from wkhtmltopdf.views import PDFTemplateView



# Create your views here.

def user_index (request):
    order = OrderProduct.objects.all().filter(user=request.user, ordered = True).order_by('-created_date')[:10]
    context = {
        'order': order,
    }
    return render( request, 'user_dashboard/index.html', context)


def order_invoice (request, product_id):
    order = OrderProduct.objects.get(id = product_id)
    context = {
        'order': order,
    }
    return render( request, 'user_dashboard/index.html', context)


# def generate_pdf(request):
#     """Generate pdf."""
#     # Model data
#     people = Product.objects.all()

class InvoicePDFView(PDFTemplateView):
    template_name = "invoice/pdf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # myinstance = get_object_or_404(Product, pk=context['pk'])
        people = Product.objects.all()
        context['people'] = people
        return context

    # # Rendered
    # html_string = render_to_string('invoice/pdf.html', {'people': people})
    # html = HTML(string=html_string)
    # result = html.write_pdf()
    # import codecs
    # # Creating http response
    # response = HttpResponse(content_type='application/pdf;')
    # response['Content-Disposition'] = 'inline; filename=product.pdf'
    # response['Content-Transfer-Encoding'] = 'binary'
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = decode(output.name, 'r', encoding='utf-8',errors='replace') 
    #     response.write(output.read())

    # return response

    #  # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()

    # # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer)

    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # p = render_to_string('invoice/pdf.html', {'people': people})

    # # Close the PDF object cleanly, and we're done.
    # # p.showPage()
    # # p.save()

    # # FileResponse sets the Content-Disposition header so that browsers
    # # present the option to save the file.
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')



