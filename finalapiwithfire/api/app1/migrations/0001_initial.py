# Generated by Django 4.2.3 on 2024-03-14 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KnownLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'known_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UnknownLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.CharField(blank=True, max_length=255, null=True)),
                ('image_name', models.CharField(blank=True, max_length=255, null=True)),
                ('image_data', models.BinaryField(blank=True, null=True)),
                ('detection_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'unknown_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Camera_Id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200)),
                ('camera_id', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status_Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_id', models.CharField(max_length=300)),
                ('camera_id', models.CharField(max_length=300)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadUrlAndImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('image_urls', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User_Id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('user_id', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]
