# Generated by Django 4.2.19 on 2025-03-15 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_business_change_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='change_password',
        ),
        migrations.AddField(
            model_name='employee',
            name='change_password',
            field=models.BooleanField(default=False),
        ),
    ]
