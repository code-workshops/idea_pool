# Generated by Django 2.0.2 on 2018-08-15 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180815_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=300, null=True, unique=True),
        ),
    ]