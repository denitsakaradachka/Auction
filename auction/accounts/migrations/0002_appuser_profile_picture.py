# Generated by Django 4.1.3 on 2022-11-27 15:06

import auction.items.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos', validators=[auction.items.validators.validate_file_less_than_5mb]),
        ),
    ]
