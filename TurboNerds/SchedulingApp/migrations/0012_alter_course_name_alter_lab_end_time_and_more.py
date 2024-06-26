# Generated by Django 5.0.4 on 2024-05-16 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulingApp', '0011_alter_lab_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(default='Course Name', max_length=30),
        ),
        migrations.AlterField(
            model_name='lab',
            name='end_time',
            field=models.TimeField(default='15:20:00'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='start_time',
            field=models.TimeField(default='13:00:00'),
        ),
        migrations.AlterField(
            model_name='section',
            name='end_time',
            field=models.TimeField(default='14:15:00'),
        ),
        migrations.AlterField(
            model_name='section',
            name='start_time',
            field=models.TimeField(default='13:00:00'),
        ),
    ]
