# Generated by Django 4.0.6 on 2022-07-09 00:08

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('is_moder', models.BooleanField(default=False)),
                ('registrationDate', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Genere',
            fields=[
                ('genere_id', models.AutoField(primary_key=True, serialize=False)),
                ('genere_name', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('instrument_id', models.AutoField(primary_key=True, serialize=False)),
                ('instrument_name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sytheseizer',
            fields=[
                ('sytheseizer_id', models.AutoField(primary_key=True, serialize=False)),
                ('sytheseizer_name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SamplePack',
            fields=[
                ('sp_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(default=0)),
                ('path', models.FilePathField(path='C:/Users/Volodi4/PycharmProjects/djangoFSAP/USERSFILES')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('genere_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.genere')),
            ],
            options={
                'unique_together': {('name', 'author')},
            },
        ),
        migrations.CreateModel(
            name='PresetPack',
            fields=[
                ('pp_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('dateAdded', models.DateTimeField(auto_now=True)),
                ('rating', models.IntegerField(default=0)),
                ('path', models.FilePathField(path='C:/Users/Volodi4/PycharmProjects/djangoFSAP/USERSFILES')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('genere_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.genere')),
                ('sytheseizer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.sytheseizer')),
            ],
            options={
                'unique_together': {('name', 'sytheseizer_id', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('sample_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('instrument_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.instrument')),
                ('sp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.samplepack')),
            ],
            options={
                'unique_together': {('sample_id', 'sp_id')},
            },
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('preset_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('instrument_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.instrument')),
                ('pp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.presetpack')),
            ],
            options={
                'unique_together': {('name', 'pp_id')},
            },
        ),
        migrations.CreateModel(
            name='FavoriteSamplePacks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.samplepack')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'sp_id')},
            },
        ),
        migrations.CreateModel(
            name='FavoritePresetPacks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.presetpack')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'pp_id')},
            },
        ),
    ]
