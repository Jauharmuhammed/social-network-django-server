# Generated by Django 4.1.3 on 2022-12-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/dpofqivee/image/upload/v1672380610/social_network/profile_picture/profile_nloi7m.jpg', max_length=255, null=True, upload_to='social_network/profile_picture'),
        ),
    ]
