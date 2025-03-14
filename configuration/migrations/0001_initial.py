# Generated by Django 4.2.19 on 2025-03-04 18:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0003_otp_alter_business_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('darkMode', models.BooleanField(default=False)),
                ('MFA', models.BooleanField(default=False)),
                ('staff_change_First_password', models.BooleanField(default=False)),
                ('force_password_Change', models.BooleanField(default=False)),
                ('lock_business', models.BooleanField(default=False)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
            ],
        ),
    ]
