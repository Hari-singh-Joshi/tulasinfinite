# Generated by Django 5.1.7 on 2025-03-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_alter_consultant_image_alter_consultant_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Disease",
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
                ("code", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("symptoms", models.TextField()),
                ("causes", models.TextField()),
                ("ayurvedic_cure", models.TextField(blank=True, null=True)),
                ("medications", models.TextField(blank=True, null=True)),
                ("yoga", models.TextField(blank=True, null=True)),
                ("siddha_remedies", models.TextField(blank=True, null=True)),
                ("acupressure_points", models.TextField(blank=True, null=True)),
                ("lifestyle_diet", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
