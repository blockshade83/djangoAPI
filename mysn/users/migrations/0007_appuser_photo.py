# Generated by Django 3.0.3 on 2022-07-31 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220724_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='photo',
            field=models.ImageField(default='default/default_profile.png', upload_to='profile'),
        ),
    ]
