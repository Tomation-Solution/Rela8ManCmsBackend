# Generated by Django 4.2 on 2023-05-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_reports_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='readmore_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
