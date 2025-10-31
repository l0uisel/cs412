# File: voter_analytics/views.py
# Author: Louise Lee, llouise@bu.edu, 10/30/2025
# Description: Defines views for voters list, detail, and graphs with reusable filtering + sticky UI state

from django.views.generic import ListView, DetailView
from django.utils.http import urlencode
from django.db.models import Count
from .models import Voter

import plotly
import plotly.graph_objs as go


class _FilterMixin:
    """Filtering + context for list and graphs."""

    def _filtered_queryset(self):
        qs = Voter.objects.all()

        # Party (exact match on stored value)
        party = self.request.GET.get("party_affiliation", "").upper()
        if party:
            qs = qs.filter(party_affiliation=party)

        # DOB year range
        min_year = self.request.GET.get("min_birth_year", "")
        if min_year:
            qs = qs.filter(date_of_birth__year__gte=int(min_year))

        max_year = self.request.GET.get("max_birth_year", "")
        if max_year:
            qs = qs.filter(date_of_birth__year__lte=int(max_year))

        # Voter score
        score = self.request.GET.get("voter_score", "")
        if score != "":
            qs = qs.filter(voter_score=int(score))

        # Election checkboxes: presence means True
        for fld in ["v20state", "v21town", "v21primary", "v22general", "v23town"]:
            if self.request.GET.get(fld):
                qs = qs.filter(**{fld: True})

        return qs

    def _filter_context(self, context):
        # Distinct parties (already stored as upcased)
        context["party_affiliations"] = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .distinct()
            .order_by("party_affiliation")
        )

        # Distinct DOB years, newest first
        years = (
            Voter.objects.exclude(date_of_birth__isnull=True)
            .values_list("date_of_birth__year", flat=True)
            .distinct()
            .order_by("-date_of_birth__year")
        )
        context["birth_years"] = years

        # Scores for dropdown
        context["scores"] = [0, 1, 2, 3, 4, 5]

        # Preserve GET params across pagination
        qd = self.request.GET.copy()
        qd.pop("page", None)
        context["querystring"] = "&" + urlencode(qd, doseq=True) if qd else ""

        return context


class VoterListView(_FilterMixin, ListView):
    """Define a view class to display voter listing with filtering"""

    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        return self._filtered_queryset().order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self._filter_context(context)


class VoterDetailView(DetailView):
    """Define a view class to show detail page for one voter."""

    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "voter"


class GraphsView(_FilterMixin, ListView):
    """Define a view class to display graphs of voter data"""

    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_queryset(self):
        return self._filtered_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._filter_context(context)

        voters = context["voters"]

        # 1) Birth year histogram
        byears = list(
            voters.exclude(date_of_birth__isnull=True).values_list(
                "date_of_birth__year", flat=True
            )
        )
        year_counts = {}
        for y in byears:
            year_counts[y] = year_counts.get(y, 0) + 1
        x_years = sorted(year_counts.keys())
        y_counts = [year_counts[y] for y in x_years]
        fig_birth = go.Bar(x=x_years, y=y_counts)
        context["graph_birth"] = plotly.offline.plot(
            {
                "data": [fig_birth],
                "layout": go.Layout(
                    title="Distribution of Voters by Birth Year",
                    xaxis_title="Year of Birth",
                    yaxis_title="Count",
                ),
            },
            auto_open=False,
            output_type="div",
        )

        # 2) Party pie
        pcounts = (
            voters.values("party_affiliation")
            .annotate(n=Count("party_affiliation"))
            .order_by("party_affiliation")
        )
        labels = [(r["party_affiliation"] or "").strip() or "(blank)" for r in pcounts]
        values = [r["n"] for r in pcounts]
        fig_party = go.Pie(labels=labels, values=values, hole=0.3)
        context["graph_party"] = plotly.offline.plot(
            {
                "data": [fig_party],
                "layout": go.Layout(title="Distribution of Voters by Party"),
            },
            auto_open=False,
            output_type="div",
        )

        # 3) Election participation bars
        elections = {
            "2020 State": voters.filter(v20state=True).count(),
            "2021 Town": voters.filter(v21town=True).count(),
            "2021 Primary": voters.filter(v21primary=True).count(),
            "2022 General": voters.filter(v22general=True).count(),
            "2023 Town": voters.filter(v23town=True).count(),
        }
        fig_elec = go.Bar(x=list(elections.keys()), y=list(elections.values()))
        context["graph_elections"] = plotly.offline.plot(
            {
                "data": [fig_elec],
                "layout": go.Layout(
                    title="Voter Participation in Elections",
                    xaxis_title="Election",
                    yaxis_title="Voters",
                ),
            },
            auto_open=False,
            output_type="div",
        )

        return context
