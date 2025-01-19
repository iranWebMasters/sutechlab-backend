from django.conf import settings
from django.db import models
from accounts.models import User
from services.models import Experiment, Test, Parameters
from .utils import generate_order_code
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display

def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # Connects letters
    bidi_text = get_display(reshaped_text)  # Converts to right-to-left
    return bidi_text

def generate_invoice(order):
    # Path for the invoice PDF file
    pdf_directory = os.path.join(settings.MEDIA_ROOT, 'invoices')
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # Path for the invoice PDF file
    pdf_file_path = os.path.join(pdf_directory, f"invoice_{order.id}.pdf")

    # Create PDF
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Register Persian font (ensure the path is correct)
    pdfmetrics.registerFont(TTFont('Persian', 'statics/fonts/Vazir.ttf'))

    # Set the font to Persian
    c.setFont("Persian", 12)

    # Title
    c.drawRightString(width - 100, height - 50, reshape_text(f"پیش فاکتور برای درخواست ID: {order.id}"))

    # User Information
    c.drawRightString(width - 100, height - 70, reshape_text(f"کاربر: {order.user.email}"))
    c.drawRightString(width - 100, height - 90, reshape_text(f"کد مشتری: {order.user.customer_code}"))
    c.drawRightString(width - 100, height - 110, reshape_text(f"نام و نام خانوادگی: {order.user.profile.first_name} {order.user.profile.last_name}"))
    c.drawRightString(width - 100, height - 130, reshape_text(f"تاریخ ثبت درخواست: {order.created_at.strftime('%Y-%m-%d')}"))
    c.drawRightString(width - 100, height - 150, reshape_text(f"وضعیت: {order.get_status_display()}"))

    y_position = height - 170  # Update y_position after user info
    c.line(50, y_position, width - 50, y_position)  # Draw line separator
    y_position -= 10  # Move down after the line

    # Experiment Information
    c.drawRightString(width - 100, y_position, reshape_text(f"آزمایش: {order.experiment.test_name if order.experiment else 'N/A'}"))
    y_position -= 20

    # Sample Information
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات نمونه‌ها:"))
    y_position -= 20

    for sample in order.sample_info.all():
        c.drawRightString(width - 120, y_position, reshape_text(f"نوع نمونه: {sample.sample_type}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"نام نمونه مشتری: {sample.customer_sample_name}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"تعداد: {sample.sample_count}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"شرایط نگهداری: {sample.storage_conditions}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"توضیحات نمونه: {sample.sample_description}"))
        y_position -= 20
        if sample.file_upload:
            c.drawRightString(width - 120, y_position, reshape_text(f"فایل تکمیلی نمونه: {sample.file_upload.url}"))
            y_position -= 20

    y_position -= 10  # Move down after the last sample info line
    c.line(50, y_position, width - 50, y_position)  # Draw line separator
    y_position -= 10  # Move down after the line

    # Test Information
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات آزمایش‌ها:"))
    y_position -= 20

    for test in order.test_info.all():
        c.drawRightString(width - 120, y_position, reshape_text(f"شناسه نمونه آزمایش: {test.user_sample.customer_sample_name}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"عنوان آزمایش: {test.test.name_fa if test.test else 'N/A'}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"تعداد تکرار آزمون: {test.repeat_count_test}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"پارامتر: {test.parameter}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"مقدار پارامتر: {test.get_parameter_values_dict()}"))  # Assuming this returns a dict
        y_position -= 20

    y_position -= 10  # Move down after the last test info line
    c.line(50, y_position, width - 50, y_position)  # Draw line separator
    y_position -= 10  # Move down after the line

    # Discount Information
    discount_info = order.discount_info  # Assuming one discount info per order
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات تخفیف:"))
    y_position -= 20
    if discount_info:
        c.drawRightString(width - 120, y_position, reshape_text(f"عضو هیات علمی: {'بله' if discount_info.is_faculty_member else 'خیر'}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"دانشجو یا کارکنان دانشگاه: {'بله' if discount_info.is_student_or_staff else 'خیر'}"))
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"متقاضی تخفیف نهادهای طرف قرارداد: {'بله' if discount_info.is_affiliated_with_institution else 'خیر'}"))
        y_position -= 20
        if discount_info.contract_party_file:
            c.drawRightString(width - 120, y_position, reshape_text(f"نام نهاد تخفیف: {discount_info.contract_party_file.url}"))

    # Finalizing PDF
    c.save()

    # Set the path in the order without 'media/'
    order.invoice_pdf = f'invoices/invoice_{order.id}.pdf'  # Only save the relative path
    order.save()  # Save the order to update the invoice_pdf field

    return pdf_file_path  # Return the path to the PDF file