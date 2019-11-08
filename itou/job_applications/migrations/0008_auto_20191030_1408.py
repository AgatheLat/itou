# Generated by Django 2.2.6 on 2019-10-30 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ("prescribers", "0006_auto_20191015_1152"),
        ("siaes", "0010_auto_20191028_1143"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("job_applications", "0007_jobapplication_siae"),
    ]

    operations = [
        migrations.RemoveField(model_name="jobapplication", name="prescriber"),
        migrations.RemoveField(
            model_name="jobapplication", name="prescriber_organization"
        ),
        migrations.RemoveField(model_name="jobapplication", name="siae"),
        migrations.AddField(
            model_name="jobapplication",
            name="sender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="job_applications_sent",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Émetteur",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="sender_kind",
            field=models.CharField(
                choices=[
                    ("job_seeker", "Demandeur d'emploi"),
                    ("prescriber", "Prescripteur"),
                    ("siae_staff", "Employeur (SIAE)"),
                ],
                default="prescriber",
                max_length=10,
                verbose_name="Type de l'émetteur",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="sender_prescriber_organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="prescribers.PrescriberOrganization",
                verbose_name="Organisation du prescripteur émettrice",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="sender_siae",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="siaes.Siae",
                verbose_name="SIAE émettrice",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="to_siae",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_applications_received",
                to="siaes.Siae",
                verbose_name="SIAE destinataire",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="job_seeker",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_applications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Demandeur d'emploi",
            ),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="state",
            field=django_xworkflows.models.StateField(
                db_index=True,
                max_length=16,
                verbose_name="État",
                workflow=django_xworkflows.models._SerializedWorkflow(
                    initial_state="new",
                    name="JobApplicationWorkflow",
                    states=[
                        "new",
                        "processing",
                        "postponed",
                        "accepted",
                        "refused",
                        "obsolete",
                    ],
                ),
            ),
        ),
    ]