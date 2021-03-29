# Generated by Django 3.1.7 on 2021-03-25 10:08

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('applied', 'Applied'), ('rejected', 'Rejected'), ('accepted', 'Accepted')], default='applied', max_length=100),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.upload_and_rename_pic),
        ),
        migrations.AlterField(
            model_name='student',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to=user.models.upload_and_rename_cv),
        ),
    ]