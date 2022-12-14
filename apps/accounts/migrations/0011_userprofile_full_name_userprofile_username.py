# Generated by Django 4.1.3 on 2022-12-15 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(default='new', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
