# Generated by Django 5.1.1 on 2024-10-09 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_boqquotationtable_warrentyyear'),
    ]

    operations = [
        migrations.AddField(
            model_name='boqquotationtable',
            name='totalUnitPrice',
            field=models.IntegerField(null=True),
        ),
    ]
