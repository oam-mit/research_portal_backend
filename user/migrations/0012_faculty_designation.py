# Generated by Django 3.1.7 on 2021-08-12 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210325_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='designation',
            field=models.CharField(choices=[('Mr', 'Mr'), ('Ms', 'Ms'), ('Mrs', 'Mrs'), ('Dr', 'Dr')], default='Mr', max_length=10),
        ),
    ]