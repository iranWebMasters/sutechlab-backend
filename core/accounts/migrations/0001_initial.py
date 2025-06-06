# Generated by Django 5.1.1 on 2025-01-05 11:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "customer_code",
                    models.CharField(blank=True, max_length=10, unique=True),
                ),
                ("created_date", models.DateField(auto_now_add=True)),
                ("updated_date", models.DateField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=250)),
                ("last_name", models.CharField(max_length=250)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="profile_images/default.jpg",
                        null=True,
                        upload_to="profile_images/",
                    ),
                ),
                ("national_id", models.CharField(max_length=10)),
                ("phone_number", models.CharField(max_length=15)),
                ("address", models.TextField()),
                ("postal_code", models.CharField(max_length=10)),
                ("created_date", models.DateField(auto_now_add=True)),
                (
                    "wallet_balance",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0.0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("updated_date", models.DateField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
