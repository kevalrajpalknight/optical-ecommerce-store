# Generated by Django 2.2.14 on 2020-10-17 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201017_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='lenses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.EyeLenses'),
        ),
    ]
