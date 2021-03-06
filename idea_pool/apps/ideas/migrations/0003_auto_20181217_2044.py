# Generated by Django 2.0.2 on 2018-12-17 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_idea_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='confidence',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='idea',
            name='content',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='idea',
            name='ease',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='idea',
            name='impact',
            field=models.IntegerField(),
        ),
    ]
