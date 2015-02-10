# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_manager', '0002_auto_20150210_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='file_field',
            field=models.FileField(storage='media', upload_to='Library'),
            preserve_default=True,
        ),
    ]
