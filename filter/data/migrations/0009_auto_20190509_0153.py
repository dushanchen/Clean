# Generated by Django 2.1 on 2019-05-09 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_productnamespecs_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productnamespecs',
            name='remark',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
