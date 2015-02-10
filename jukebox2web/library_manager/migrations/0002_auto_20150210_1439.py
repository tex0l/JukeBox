# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='file_field',
            field=models.FileField(upload_to='Library'),
            preserve_default=True,
        ),
    ]
