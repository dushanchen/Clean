# Generated by Django 2.1 on 2019-05-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_productnamespecs_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='productnamespecs',
            name='unit',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
