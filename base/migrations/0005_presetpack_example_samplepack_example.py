# Generated by Django 4.0.6 on 2022-07-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_presetpack_path_alter_samplepack_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='presetpack',
            name='example',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='samplepack',
            name='example',
            field=models.CharField(default='', max_length=300),
        ),
    ]
