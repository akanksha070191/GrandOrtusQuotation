# Generated by Django 5.1.1 on 2024-10-14 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_boqquotationtable_currentdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='boqquotationtable',
            name='quotationType',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
