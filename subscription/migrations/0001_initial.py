# Generated by Django 4.2.19 on 2025-03-03 23:51

from django.db import migrations, models
import django.db.models.deletion
import subscription.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plan', '0001_initial'),
        ('business', '0003_otp_alter_business_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expiry_date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_recurring', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('ACTIVE', 'Active'), ('EXPIRED', 'Expired')], default='ACTIVE', max_length=12)),
                ('payment_status', models.CharField(choices=[('NOT_PAID', 'Not Paid'), ('PAID', 'Paid')], default='NOT_PAID', max_length=10)),
                ('cycle', models.CharField(choices=[('YEARLY', 'Yearly'), ('MONTHLY', 'Monthly')], default='MONTHLY', max_length=10)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
                ('plan', models.ForeignKey(blank=True, default=subscription.models.get_default_plan, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='plan.plan')),
            ],
        ),
    ]
