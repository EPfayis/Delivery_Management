# Generated by Django 3.0 on 2019-12-20 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderDetails', '0002_auto_20191220_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblstatusdetails',
            old_name='sta2us',
            new_name='status',
        ),
    ]
