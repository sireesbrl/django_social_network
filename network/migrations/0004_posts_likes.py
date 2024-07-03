# Generated by Django 4.2.11 on 2024-06-27 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0003_remove_posts_liked_by_remove_posts_likes_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="posts",
            name="likes",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="network.likes",
            ),
        ),
    ]
