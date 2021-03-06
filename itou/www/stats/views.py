from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.utils import timezone

from django.db.models import Q
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Count

from itou.siaes.models import Siae
from itou.users.models import User
from itou.job_applications.models import JobApplication, JobApplicationWorkflow


def inject_siaes_subset_total_and_by_kind(data, kpi_name, siaes_subset, visible=True):
    if "siaes_by_kind" not in data:
        data["siaes_by_kind"] = {}
        data["siaes_by_kind"]["categories"] = Siae.KIND_CHOICES
        data["siaes_by_kind"]["series"] = []

    siaes_by_kind_as_list = (
        siaes_subset.values("kind")
        .annotate(total=Count("pk", distinct=True))
        .order_by("kind")
    )

    siaes_by_kind_as_dict = {}
    for item in siaes_by_kind_as_list:
        siaes_by_kind_as_dict[item["kind"]] = item["total"]

    serie_values = []
    for kind_choice in data["siaes_by_kind"]["categories"]:
        kind = kind_choice[0]
        if kind in siaes_by_kind_as_dict:
            serie_values.append(siaes_by_kind_as_dict[kind])
        else:
            serie_values.append(0)

    total = siaes_subset.count()
    if sum(serie_values) != total:
        raise ValueError("Inconsistent results.")

    data["siaes_by_kind"]["series"].append(
        {"name": kpi_name, "values": serie_values, "total": total, "visible": visible}
    )
    return data


def stats(request, template_name="stats/stats.html"):
    data = {}

    # --- Siae stats.

    kpi_name = "Siaes à ce jour"
    siaes_subset = Siae.active_objects
    data = inject_siaes_subset_total_and_by_kind(data, kpi_name, siaes_subset)

    kpi_name = "Siaes ayant au moins un utilisateur à ce jour"
    siaes_subset = Siae.active_objects.filter(
        siaemembership__user__is_active=True
    ).distinct()
    data = inject_siaes_subset_total_and_by_kind(
        data, kpi_name, siaes_subset, visible=False
    )

    kpi_name = "Siaes ayant au moins une FDP à ce jour"
    siaes_subset = Siae.active_objects.exclude(
        job_description_through__isnull=True
    ).distinct()
    data = inject_siaes_subset_total_and_by_kind(
        data, kpi_name, siaes_subset, visible=False
    )

    kpi_name = "Siaes ayant au moins une FDP active à ce jour"
    siaes_subset = Siae.active_objects.filter(
        job_description_through__is_active=True
    ).distinct()
    data = inject_siaes_subset_total_and_by_kind(
        data, kpi_name, siaes_subset, visible=False
    )

    kpi_name = "Siaes ayant au moins un utilisateur et une FDP à ce jour"
    siaes_subset = (
        Siae.active_objects.filter(siaemembership__user__is_active=True)
        .exclude(job_description_through__isnull=True)
        .distinct()
    )
    data = inject_siaes_subset_total_and_by_kind(
        data, kpi_name, siaes_subset, visible=False
    )

    kpi_name = "Siaes ayant au moins un utilisateur et une FDP active à ce jour"
    siaes_subset = (
        Siae.active_objects.filter(siaemembership__user__is_active=True)
        .filter(job_description_through__is_active=True)
        .distinct()
    )
    data = inject_siaes_subset_total_and_by_kind(
        data, kpi_name, siaes_subset, visible=False
    )

    kpi_name = "Siaes actives à ce jour"
    today = timezone.localtime(timezone.now()).date()
    two_weeks_ago = today + relativedelta(weeks=-2)
    siaes_subset = Siae.active_objects.filter(
        Q(updated_at__date__gte=two_weeks_ago)
        | Q(created_at__date__gte=two_weeks_ago)
        | Q(siaemembership__user__date_joined__date__gte=two_weeks_ago)
        | Q(job_description_through__created_at__date__gte=two_weeks_ago)
        | Q(job_description_through__updated_at__date__gte=two_weeks_ago)
        | Q(job_applications_received__created_at__date__gte=two_weeks_ago)
        | Q(job_applications_received__updated_at__date__gte=two_weeks_ago)
    ).distinct()
    data = inject_siaes_subset_total_and_by_kind(data, kpi_name, siaes_subset)

    kpi_name = "Siaes ayant au moins une embauche"
    siaes_subset = Siae.active_objects.filter(
        job_applications_received__state=JobApplicationWorkflow.STATE_ACCEPTED
    ).distinct()
    data = inject_siaes_subset_total_and_by_kind(data, kpi_name, siaes_subset)

    # --- Candidate stats.

    data["total_job_applications"] = JobApplication.objects.count()

    data["total_hirings"] = JobApplication.objects.filter(
        state=JobApplicationWorkflow.STATE_ACCEPTED
    ).count()

    data["job_applications_per_creation_week"] = get_total_per_week(
        JobApplication.objects, date_field="created_at", total_expression=Count("pk")
    )

    data["hirings_per_creation_week"] = get_total_per_week(
        JobApplication.objects.filter(state=JobApplicationWorkflow.STATE_ACCEPTED),
        date_field="created_at",
        total_expression=Count("pk"),
    )

    data["job_applications_per_sender_kind"] = get_pie_chart_data_per_sender_kind(
        JobApplication.objects
    )

    data["hirings_per_sender_kind"] = get_pie_chart_data_per_sender_kind(
        JobApplication.objects.filter(state=JobApplicationWorkflow.STATE_ACCEPTED)
    )

    # --- Prescriber stats.

    data["total_prescriber_users"] = User.objects.filter(is_prescriber=True).count()

    data["prescriber_users_per_creation_week"] = get_total_per_week(
        User.objects.filter(is_prescriber=True),
        date_field="date_joined",
        total_expression=Count("pk"),
    )

    # Active prescriber means created at least one job
    # application in the given timeframe.
    data["active_prescriber_users_per_week"] = get_total_per_week(
        JobApplication.objects.filter(
            sender_kind=JobApplication.SENDER_KIND_PRESCRIBER
        ),
        date_field="created_at",
        total_expression=Count("sender_id", distinct=True),
    )

    context = {"data": data}
    return render(request, template_name, context)


def get_pie_chart_data_per_sender_kind(queryset):
    total_per_sender_kind_as_list = (
        queryset.values("sender_kind")
        .annotate(total=Count("pk", distinct=True))
        .order_by("sender_kind")
    )
    total_per_sender_kind_as_dict = {
        item["sender_kind"]: item["total"] for item in total_per_sender_kind_as_list
    }
    sender_kind_choices_as_dict = {
        item[0]: item[1] for item in JobApplication.SENDER_KIND_CHOICES
    }
    total_authorized_prescribers = (
        queryset.filter(sender_prescriber_organization__is_authorized=True)
        .distinct()
        .count()
    )

    if (
        total_per_sender_kind_as_dict[JobApplication.SENDER_KIND_PRESCRIBER]
        < total_authorized_prescribers
    ):
        raise ValueError("Inconsistent prescriber data.")

    pie_chart_data = [
        {
            "name": sender_kind_choices_as_dict[JobApplication.SENDER_KIND_JOB_SEEKER],
            "value": total_per_sender_kind_as_dict[
                JobApplication.SENDER_KIND_JOB_SEEKER
            ],
        },
        {
            "name": "Prescripteur non habilité",
            "value": total_per_sender_kind_as_dict[
                JobApplication.SENDER_KIND_PRESCRIBER
            ]
            - total_authorized_prescribers,
        },
        {"name": "Prescripteur habilité", "value": total_authorized_prescribers},
        {
            "name": sender_kind_choices_as_dict[JobApplication.SENDER_KIND_SIAE_STAFF],
            "value": total_per_sender_kind_as_dict[
                JobApplication.SENDER_KIND_SIAE_STAFF
            ],
        },
    ]
    return pie_chart_data


def get_total_per_week(queryset, date_field, total_expression):
    result = list(
        queryset.annotate(year=ExtractYear(date_field))
        .annotate(week=ExtractWeek(date_field))
        .values("year", "week")
        .annotate(total=total_expression)
        .order_by("year", "week")
    )
    return result
