# Generated by Django 2.2.4 on 2019-09-26 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("prescribers", "0005_auto_20190926_1454")]

    operations = [
        migrations.AlterModelOptions(
            name="prescriberorganization",
            options={
                "verbose_name": "Organisation",
                "verbose_name_plural": "Organisations",
            },
        )
    ]