# Generated by Django 3.0.3 on 2022-07-31 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220731_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='photo',
            field=models.ImageField(default='default/default_profile.png', upload_to=''),
        ),
    ]
