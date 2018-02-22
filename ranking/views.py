from django.views.generic import ListView, View, DetailView
from django.shortcuts import redirect

from datetime import date, datetime

from django_ical.views import ICalFeed

from .models import *


class EventsView(ListView):
    """ Display events of today and in the near future. """
    template_name = 'ranking/index.html'
    model = Match
    context_object_name = 'events'
    queryset = Match.objects \
        .filter(match_date__gte=date.today()) \
        .order_by('match_date')[:5]

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['title'] = 'Events'
        return context


class AllEventsView(EventsView):
    template_name = 'ranking/index.html'
    queryset = Match.objects.all() \
        .order_by('match_date')


class EventDetailView(DetailView):
    model = Match
    context_object_name = 'event'


class ResultView(ListView):
    model = Result
    context_object_name = 'results'

    def get_queryset(self):
        event = self.kwargs['pk']
        queryset = super(ResultView, self).get_queryset() \
            .filter(match_id=event) \
            .order_by('-count')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['match'] = self.get_queryset()[0].match
        return context


class MyResults(ListView):
    model = Result
    context_object_name = 'results'
    template_name = 'ranking/my_results.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return redirect('/admin')
        else:
            return super(MyResults, self).get(*args, **kwargs)

    def get_queryset(self):
        return super(MyResults, self).get_queryset() \
                .filter(shooter=self.request.user.shooter)


class ExternalMatches(ListView):
    model = Match
    context_object_name = 'events'
    template_name = 'ranking/external_list.html'

    def get_queryset(self):
        queryset = super(ExternalMatches, self).get_queryset() \
            .filter(organizer_id__gt=1)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ExternalMatches, self).get_context_data(**kwargs)
        context['participations'] = Participation.objects.filter(shooter=self.request.user.shooter)

        remaining = [match for match in self.get_queryset()]
        for participation in context['participations']:
            if participation.match in remaining:
                remaining.remove(participation.match)
        context['remaining'] = remaining

        return context


class MatchSubscription(View):
    def get(self, request, event_id):
        part = Participation()
        part.shooter = request.user.shooter
        part.match = Match.objects.get(pk=event_id)
        part.save()
        return redirect('external_matches')


class MatchUnsubscription(View):
    def get(self, request, part_id):
        part = Participation.objects.get(pk=part_id)
        part.delete()
        return redirect('external_matches')


class ApplySupervisor(View):
    def get(self, request, event_id):
        match = Match.objects.get(pk=event_id)
        match.supervisor = request.user.shooter
        match.save()
        return redirect('event', pk=event_id)


class EventFeed(ICalFeed):
    """
    Event Calendar
    """
    product_id = '-//ps-niedergoesgen.ch//Veranstaltungen//DE'
    timezone = 'UTC+1'
    file_name = "event.ics"

    def items(self):
        return Match.objects.filter(match_date__gte=date.today()).order_by('-match_date')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return datetime.combine(item.match_date, item.begins)

    def item_end_datetime(self, item):
        return datetime.combine(item.match_date, item.ends)
