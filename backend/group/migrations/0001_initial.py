# Generated by Django 3.2.11 on 2022-01-29 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('short_description', models.TextField()),
                ('description', utils.models.RichTextField()),
                ('is_official', models.BooleanField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('admin_members', models.ManyToManyField(related_name='admin_groups', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_group',
            },
        ),
        migrations.CreateModel(
            name='GroupRegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('short_description', models.TextField()),
                ('description', utils.models.RichTextField()),
                ('is_official', models.BooleanField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_registration_request',
            },
        ),
        migrations.CreateModel(
            name='GroupApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', utils.models.RichTextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.usergroup')),
            ],
            options={
                'db_table': 'group_application',
            },
        ),
    ]