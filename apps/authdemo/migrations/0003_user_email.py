# Generated by Django 2.0.5 on 2018-09-22 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authdemo', '0002_remove_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
