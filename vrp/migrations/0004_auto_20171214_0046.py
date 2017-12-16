# Generated by Django 2.0 on 2017-12-14 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vrp', '0003_auto_20171213_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(decimal_places=14, default=48.721287, max_digits=16),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(decimal_places=14, default=18.5491726, max_digits=16),
        ),
    ]
