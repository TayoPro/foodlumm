# Generated by Django 4.0.2 on 2022-03-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_remove_profile_id_profile_cart_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cart_num',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
