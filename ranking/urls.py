from django.urls import include, path
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
	path('', EventsView.as_view(), name='events_list'),
	path('all', AllEventsView.as_view(), name='events_list'),
	path('feed.ics', EventFeed(), name='events_ical'),
    path('match/<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('results/<int:pk>', ResultView.as_view(), name='result_detail'),
    path('extern/', login_required(ExternalMatches.as_view()), name='external_matches'),
    path('teilnehmen/<int:event_id>', login_required(MatchSubscription.as_view()), name='subscribe_match'),
    path('abmelden/<int:part_id>', login_required(MatchUnsubscription.as_view()), name='unsubscribe_match'),
    path('my_results', login_required(MyResults.as_view()), name='my_results'),
]
