# Generated by Django 2.2.14 on 2020-10-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_eyelenses_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='in_process_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]