# Generated by Django 5.1.1 on 2024-10-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_boqquotationtable_totalamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='boqquotationtable',
            name='currentDate',
            field=models.DateField(null=True),
        ),
    ]
