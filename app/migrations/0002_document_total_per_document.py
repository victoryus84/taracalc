# Generated by Django 3.2 on 2023-07-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='total_per_document',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
