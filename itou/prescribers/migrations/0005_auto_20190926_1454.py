# Generated by Django 2.2.4 on 2019-09-26 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("prescribers", "0004_auto_20190926_1011")]

    operations = [
        migrations.AddField(
            model_name="prescriberorganization",
            name="description",
            field=models.TextField(blank=True, verbose_name="Description"),
        ),
        migrations.AddField(
            model_name="prescriberorganization",
            name="website",
            field=models.URLField(blank=True, verbose_name="Site web"),
        ),
    ]