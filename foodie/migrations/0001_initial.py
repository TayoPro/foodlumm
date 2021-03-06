# Generated by Django 4.0.2 on 2022-02-03 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='variety.jpg', upload_to='variety')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Variety',
                'verbose_name_plural': 'Varieties',
                'db_table': 'variety',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.CharField(max_length=100)),
                ('menu', models.TextField()),
                ('image', models.ImageField(default='meal.jpg', upload_to='meal')),
                ('spicy', models.CharField(choices=[('Not', 'Not'), ('Mild', 'Mild'), ('Medium', 'Medium'), ('Hot', 'Hot'), ('Extra Hot', 'Extra Hot')], default='Medium', max_length=100)),
                ('time', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('breakfast', models.BooleanField()),
                ('lunch', models.BooleanField()),
                ('dinner', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('variety', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.variety')),
            ],
            options={
                'verbose_name': 'Meal',
                'verbose_name_plural': 'Meals',
                'db_table': 'meal',
                'managed': True,
            },
        ),
    ]
