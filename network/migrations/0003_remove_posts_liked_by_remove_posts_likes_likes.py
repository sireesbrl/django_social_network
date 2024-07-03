# Generated by Django 4.2.11 on 2024-06-27 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_follows"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="posts",
            name="liked_by",
        ),
        migrations.RemoveField(
            model_name="posts",
            name="likes",
        ),
        migrations.CreateModel(
            name="Likes",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked",
                        to="network.posts",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="liked_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]