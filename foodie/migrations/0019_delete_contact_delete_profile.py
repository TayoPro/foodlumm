# Generated by Django 4.0.2 on 2022-02-23 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0018_remove_shipping_paidorder_remove_shopcart_meal_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
