# Generated by Django 3.1.2 on 2020-11-05 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201101_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blood_group',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]