from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^results/(?P<event_id>\d+)/', ResultView.as_view(), name='result_detail'),
    url(r'^extern/', login_required(ExternalMatches.as_view()), name='external_matches'),
    url(r'^teilnehmen/(?P<event_id>\d+)/', login_required(MatchSubscription.as_view()), name='subscribe_match'),
    url(r'^abmelden/(?P<part_id>\d+)/', login_required(MatchUnsubscription.as_view()), name='unsubscribe_match'),
    url(r'^my_results/', login_required(MyResults.as_view()), name='my_results'),
]
