# Generated by Django 5.1.4 on 2025-01-27 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_boqquotationtable_productslno'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendorDetails',
            fields=[
                ('SlNo', models.AutoField(primary_key=True, serialize=False)),
                ('vendorName', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255, null=True)),
                ('product', models.CharField(max_length=255, null=True)),
                ('contactName', models.CharField(max_length=255, null=True)),
                ('number', models.CharField(max_length=255, null=True)),
                ('emailID', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'vendorDetails',
                'managed': False,
            },
        ),
    ]
