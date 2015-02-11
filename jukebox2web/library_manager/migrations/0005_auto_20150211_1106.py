# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_manager', '0004_auto_20150211_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='file_field',
            field=models.FileField(upload_to=b'Library/'),
            preserve_default=True,
        ),
    ]
