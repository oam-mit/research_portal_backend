# Generated by Django 3.1.7 on 2021-03-03 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='time_of_submission',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]