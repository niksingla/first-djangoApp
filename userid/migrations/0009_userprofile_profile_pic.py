# Generated by Django 4.0.2 on 2022-03-20 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userid', '0008_remove_userprofile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', upload_to='images/'),
        ),
    ]