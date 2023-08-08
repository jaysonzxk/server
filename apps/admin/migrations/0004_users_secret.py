# Generated by Django 3.2.12 on 2023-08-08 17:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_useraddr_uservipcard_vipcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='secret',
            field=models.CharField(default=uuid.uuid4, max_length=255, verbose_name='加密秘钥'),
        ),
    ]
