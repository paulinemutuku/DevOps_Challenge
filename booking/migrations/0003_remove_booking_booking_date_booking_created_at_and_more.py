# Generated by Django 4.2.20 on 2025-03-31 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("booking", "0002_fitnessclass_category_userprofile_bio_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="booking_date",
        ),
        migrations.AddField(
            model_name="booking",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="fitnessclass",
            name="capacity",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="fitnessclass",
            name="category",
            field=models.CharField(default="general", max_length=50),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="preferred_categories",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="userprofile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="userprofile",
            constraint=models.UniqueConstraint(
                fields=("user",), name="unique_user_profile"
            ),
        ),
    ]
