# Generated by Django 4.0 on 2024-03-07 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_userdata_generated_uuid_userprofile_generated_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
