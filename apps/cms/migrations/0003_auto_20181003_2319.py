# Generated by Django 2.0.5 on 2018-10-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='thumbnail',
            field=models.URLField(max_length=800),
        ),
    ]
