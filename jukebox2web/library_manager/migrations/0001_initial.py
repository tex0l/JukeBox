# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letter', models.IntegerField(verbose_name='letter')),
                ('number', models.IntegerField(verbose_name='number')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('artist', models.CharField(max_length=100, verbose_name='artist')),
                ('file_field', models.FileField(upload_to='/Library/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
