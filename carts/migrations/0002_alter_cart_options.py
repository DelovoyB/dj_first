# Generated by Django 5.1a1 on 2024-07-02 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ('-created_timestamp',), 'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзины'},
        ),
    ]
