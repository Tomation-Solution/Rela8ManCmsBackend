# Generated by Django 4.2 on 2023-08-15 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0007_whyweareunique_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='ourmembers',
            name='description',
            field=models.TextField(blank=True, default='A Member of Man', null=True),
        ),
    ]
