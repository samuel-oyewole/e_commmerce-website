# Generated by Django 3.1.3 on 2020-11-27 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BUY', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='state',
            field=models.CharField(default=True, max_length=200),
        ),
    ]
