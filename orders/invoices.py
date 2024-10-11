# userpanel/invoices.py
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_invoice(req):
    # مسیر فایل PDF پیش‌فاکتور
    pdf_file_path = f"media/invoices/invoice_{req.id}.pdf"

    # ایجاد PDF
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # نوشتن اطلاعات در PDF به زبان فارسی
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, f"پیش فاکتور برای درخواست ID: {req.id}")
    c.drawString(100, height - 120, f"کاربر: {req.user.email}")
    c.drawString(100, height - 140, f"نام و نام خانوادگی: {req.user.profile.first_name} {req.user.profile.last_name}")
    c.drawString(100, height - 160, f"آزمایش: {req.experiment.test_name}")
    c.drawString(100, height - 180, f"تاریخ درخواست: {req.request_info.submission_date}")

    # نوشتن اطلاعات نمونه‌ها
    y_position = height - 220
    c.drawString(100, y_position, "اطلاعات نمونه‌ها:")
    for sample in req.sample_info.all():
        y_position -= 20
        c.drawString(120, y_position, f"نوع نمونه: {sample.sample_type}, نام نمونه: {sample.customer_sample_name}, تعداد: {sample.sample_count}")

    # ذخیره PDF
    c.save()

    return pdf_file_path  # مسیر فایل PDF را برگردانید
