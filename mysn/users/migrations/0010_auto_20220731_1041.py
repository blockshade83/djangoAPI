# Generated by Django 3.0.3 on 2022-07-31 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20220731_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='photo',
            field=models.ImageField(default='default/default_profile.png', upload_to='profile'),
        ),
    ]
