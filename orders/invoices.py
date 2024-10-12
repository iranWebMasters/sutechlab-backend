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

    # Title
    c.drawRightString(width - 100, height - 50, reshape_text(f"پیش فاکتور برای درخواست ID: {req.id}"))

    # User Information
    c.drawRightString(width - 100, height - 70, reshape_text(f"کاربر: {req.user.email}"))
    c.drawRightString(width - 100, height - 90, reshape_text(f"کد مشتری: {req.user.customer_code}"))
    c.drawRightString(width - 100, height - 110, reshape_text(f"نام و نام خانوادگی: {req.user.profile.first_name} {req.user.profile.last_name}"))
    c.drawRightString(width - 100, height - 130, reshape_text(f"تاریخ ثبت درخواست: {req.submission_date}"))
    c.drawRightString(width - 100, height - 150, reshape_text(f"وضعیت: {req.get_status_display()}"))

    y_position = height - 170  # Update y_position after user info
    c.line(50, y_position, width - 50, y_position)  # Draw line separator
    y_position -= 10  # Move down after the line

    # Experiment Information
    c.drawRightString(width - 100, y_position, reshape_text(f"آزمایش: {req.experiment.test_name if req.experiment else 'N/A'}"))
    y_position -= 20

    # Sample Information
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات نمونه‌ها:"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"نوع نمونه: {req.sample_type}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"نام نمونه مشتری: {req.customer_sample_name}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"تعداد: {req.sample_count}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"توضیحات اضافی: {req.additional_info}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"نمونه فاسدشدنی: {'بله' if req.is_perishable else 'خیر'}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"تاریخ انقضا: {req.expiration_date if req.expiration_date else 'N/A'}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"نمونه برگشت داده شده: {'بله' if req.sample_return else 'خیر'}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"مدت زمان نگهداری: {req.storage_duration} {req.storage_duration_unit if req.storage_duration_unit else ''}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"شرایط نگهداری: {req.storage_conditions}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"توضیحات نمونه: {req.sample_description}"))
    y_position -= 20
    if req.file_upload:
        c.drawRightString(width - 120, y_position, reshape_text(f"فایل تکمیلی نمونه: {req.file_upload.url}"))

    y_position -= 10  # Move down after the last sample info line
    c.line(50, y_position, width - 50, y_position)  # Draw line separator
    y_position -= 10  # Move down after the line

    # Test Information
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات آزمایش‌ها:"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"شناسه نمونه آزمایش: {req.user_sample}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"عنوان آزمایش: {req.test.name_fa if req.test else 'N/A'}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"تعداد تکرار آزمون: {req.repeat_count_test}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"پارامتر: {req.parameter}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"مقدار پارامتر: {req.parameter_value}"))

    y_position -= 10  # Move down after the last test info line
    c.line(50, y_position, width - 50, y_position)  # Draw line separator
    y_position -= 10  # Move down after the line

    # Discount Information
    discount_info = req.discount_institution_name
    c.drawRightString(width - 100, y_position, reshape_text("اطلاعات تخفیف:"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"عضو هیات علمی: {'بله' if req.is_faculty_member else 'خیر'}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"دانشجو یا کارکنان دانشگاه: {'بله' if req.is_student_or_staff else 'خیر'}"))
    y_position -= 20
    c.drawRightString(width - 120, y_position, reshape_text(f"متقاضی تخفیف نهادهای طرف قرارداد: {'بله' if req.is_affiliated_with_institution else 'خیر'}"))
    if discount_info:
        y_position -= 20
        c.drawRightString(width - 120, y_position, reshape_text(f"نام نهاد تخفیف: {discount_info}"))

    # Finalizing PDF
    c.save()

    # Set the path in the request without 'media/'
    req.invoice_pdf = f'invoices/invoice_{req.id}.pdf'  # Only save the relative path
    req.save()  # Save the request to update the invoice_pdf field

    return pdf_file_path  # Return the path to the PDF file
