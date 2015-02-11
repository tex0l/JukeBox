# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_manager', '0003_auto_20150210_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='file_field',
            field=models.FileField(storage=b'media/', upload_to=b'Library/'),
            preserve_default=True,
        ),
    ]
