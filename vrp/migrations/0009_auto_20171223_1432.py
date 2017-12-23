# Generated by Django 2.0 on 2017-12-23 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vrp', '0008_auto_20171216_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_number', models.IntegerField()),
                ('distance', models.DecimalField(decimal_places=2, max_digits=7)),
                ('duration', models.DecimalField(decimal_places=2, max_digits=7)),
                ('instructions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vrp.Address')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vrp.Route')),
            ],
            options={
                'ordering': ['route', 'sequence'],
            },
        ),
        migrations.AlterField(
            model_name='tour',
            name='end_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_end', to='vrp.Address'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='start_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_start', to='vrp.Address'),
        ),
        migrations.AddField(
            model_name='route',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vrp.Tour'),
        ),
        migrations.AddField(
            model_name='route',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vrp.Vehicle'),
        ),
        migrations.AlterUniqueTogether(
            name='stop',
            unique_together={('route', 'sequence')},
        ),
    ]
