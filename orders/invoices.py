from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display
from django.conf import settings
import os

def reshape_text(text):
    # Convert Persian text for proper rendering in PDF (RTL and reshaped)
    reshaped_text = arabic_reshaper.reshape(text)  # Connects letters
    bidi_text = get_display(reshaped_text)  # Converts to right-to-left
    return bidi_text

def generate_invoice(req):
    # Path for the invoice PDF file
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'invoices', f"invoice_{req.id}.pdf")


    # Create PDF
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Register Persian font (ensure the path is correct)
    pdfmetrics.registerFont(TTFont('Persian', 'statics/fonts/Vazir.ttf'))

    # Set the font to Persian
    c.setFont("Persian", 12)

    # Right-align and write information in the PDF in Persian
    c.drawRightString(width - 100, height - 100, reshape_text(f"پیش فاکتور برای درخواست ID: {req.id}"))
    c.drawRightString(width - 100, height - 120, reshape_text(f"کاربر: {req.user.email}"))
    c.drawRightString(width - 100, height - 140, reshape_text(f"نام و نام خانوادگی: {req.user.profile.first_name} {req.user.profile.last_name}"))
    c.drawRightString(width - 100, height - 160, reshape_text(f"آزمایش: {req.experiment.test_name}"))
    c.drawRightString(width - 100, height - 180, reshape_text(f"تاریخ درخواست: {req.request_info.submission_date}"))

    # Write sample information, also right-aligned
    y_position = height - 220
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات نمونه‌ها:"))
    for sample in req.sample_info.all():
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"نوع نمونه: {sample.sample_type}, نام نمونه: {sample.customer_sample_name}, تعداد: {sample.sample_count}"))

    # Save the PDF
    c.save()

    # Set the path in the request without 'media/'
    req.invoice_pdf = f'invoices/invoice_{req.id}.pdf'  # Only save the relative path
    req.save()  # Save the request to update the invoice_pdf field

    return pdf_file_path  # Return the path to the PDF file
