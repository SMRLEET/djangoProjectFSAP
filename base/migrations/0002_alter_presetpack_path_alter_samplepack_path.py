# Generated by Django 4.0.6 on 2022-07-09 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presetpack',
            name='path',
            field=models.FileField(blank=True, upload_to='userfiles'),
        ),
        migrations.AlterField(
            model_name='samplepack',
            name='path',
            field=models.FileField(blank=True, upload_to='userfiles'),
        ),
    ]