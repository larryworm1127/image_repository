# Generated by Django 4.0.1 on 2022-01-14 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_imagemetadata_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemetadata',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
