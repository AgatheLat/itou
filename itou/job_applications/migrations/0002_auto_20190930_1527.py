# Generated by Django 2.2.4 on 2019-09-30 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("job_applications", "0001_initial"),
        ("siaes", "0001_initial"),
        ("jobs", "0002_create_full_text_trigger"),
        ("prescribers", "0002_auto_20190930_1527"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplicationtransitionlog",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="job_seeker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_applications_sent",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Demandeur d'emploi",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="jobs",
            field=models.ManyToManyField(
                blank=True, to="jobs.Appellation", verbose_name="Métiers recherchés"
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="prescriber",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="job_applications_prescribed",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Prescripteur",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="prescriber_organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="prescribers.PrescriberOrganization",
                verbose_name="Organisation du prescripteur",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="siae",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_applications_received",
                to="siaes.Siae",
                verbose_name="SIAE",
            ),
        ),
    ]