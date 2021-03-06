# Generated by Django 2.1 on 2019-05-07 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20190506_0407'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductNameSpecs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('specs', models.CharField(max_length=100)),
                ('level', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '商品类目二',
                'verbose_name_plural': '商品类目二',
            },
        ),
    ]
