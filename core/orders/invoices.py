from django.template.loader import render_to_string
from xhtml2pdf import pisa
import jdatetime
import os
from django.conf import settings
import arabic_reshaper
from bidi.algorithm import get_display
from website.models import Contact
from django.contrib.staticfiles import finders


def fetch_resources(uri, rel):
    if uri.startswith("http://") or uri.startswith("https://"):
        return uri
    if uri.startswith(settings.STATIC_URL):
        path = uri.replace(settings.STATIC_URL, "")
        # Ensure that the full absolute path is returned
        return os.path.join(settings.STATIC_ROOT, path)
    return None


def generate_invoice(order):
    # مسیر ذخیره فایل PDF
    pdf_directory = os.path.join(settings.MEDIA_ROOT, "invoices")
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    pdf_file_path = os.path.join(pdf_directory, f"invoice_{order.id}.pdf")

    # داده‌های لازم برای قالب
    creation_date = jdatetime.datetime.fromgregorian(date=order.created_at).strftime(
        "%Y/%m/%d"
    )
    user = order.user
    contact = Contact.objects.first()

    # بارگذاری HTML از فایل
    html_content = render_to_string(
        "orders/invoice_template.html",
        {
            "order": order,
            "creation_date": creation_date,
            "user": user,
            "contact": contact,
        },
    )

    # تابع تبدیل HTML به PDF
    def convert_html_to_pdf(source_html, output_filename):
        with open(output_filename, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                source_html, dest=result_file, link_callback=fetch_resources
            )
        return pisa_status.err

    # ایجاد فایل PDF
    convert_html_to_pdf(html_content, pdf_file_path)

    # ذخیره مسیر PDF در مدل سفارش
    order.invoice_pdf = f"invoices/invoice_{order.id}.pdf"
    order.save()

    return pdf_file_path
