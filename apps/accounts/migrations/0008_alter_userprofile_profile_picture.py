# Generated by Django 4.1.3 on 2022-12-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_picture/profile.png', null=True, upload_to='profile_picture'),
        ),
    ]
