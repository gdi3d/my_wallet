# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20150830_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(related_name='item_tags', to='wallet.Tag', blank=True),
            preserve_default=True,
        ),
    ]
