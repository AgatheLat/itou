# Generated by Django 2.2.4 on 2019-09-30 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("siaes", "0004_auto_20190930_1115")]

    operations = [
        migrations.RemoveField(model_name="siaejobdescription", name="custom_title"),
        migrations.AddField(
            model_name="siaejobdescription",
            name="custom_name",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Nom personnalisé"
            ),
        ),
    ]