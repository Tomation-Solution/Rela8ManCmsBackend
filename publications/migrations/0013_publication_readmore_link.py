# Generated by Django 4.2 on 2023-05-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0012_publication_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='readmore_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
