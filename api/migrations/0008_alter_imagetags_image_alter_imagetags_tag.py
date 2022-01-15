# Generated by Django 4.0.1 on 2022-01-15 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_imagemetadata_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetags',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.imagemetadata'),
        ),
        migrations.AlterField(
            model_name='imagetags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.tag'),
        ),
    ]