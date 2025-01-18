# Generated by Django 5.1.1 on 2024-10-01 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogInUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=250)),
                ('lastName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('phoneNumber', models.IntegerField(max_length=10)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
