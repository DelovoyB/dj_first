# Generated by Django 5.0 on 2024-07-01 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='created_timestamp',
        ),
    ]
