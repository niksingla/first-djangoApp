# Generated by Django 4.0.2 on 2022-03-01 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userid', '0004_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]