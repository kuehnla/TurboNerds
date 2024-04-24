from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulingApp', '0003_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='lab_name',
            field=models.CharField(default='lab 1', max_length=3),
        ),
        migrations.AddField(
            model_name='section',
            name='section_name',
            field=models.CharField(default='Section 1', max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=20),
        ),
    ]
