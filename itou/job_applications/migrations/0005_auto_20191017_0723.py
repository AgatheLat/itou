# Generated by Django 2.2.6 on 2019-10-17 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("job_applications", "0004_jobapplication_prescriber_organization")]

    operations = [
        migrations.AlterField(
            model_name="jobapplication",
            name="updated_at",
            field=models.DateTimeField(
                blank=True,
                db_index=True,
                null=True,
                verbose_name="Date de modification",
            ),
        )
    ]
