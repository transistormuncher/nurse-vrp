# Generated by Django 2.0 on 2017-12-23 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vrp', '0009_auto_20171223_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='point_list',
            field=models.TextField(blank=True, null=True),
        ),
    ]
