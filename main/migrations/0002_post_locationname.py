# Generated by Django 2.2.28 on 2024-03-03 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='locationName',
            field=models.CharField(default='Unknown', editable=False, max_length=100),
        ),
    ]