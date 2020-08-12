from django.urls import path
from ..views.tournament_views import Tournaments, TournamentDetail
from ..views.player_views import Players
from ..views.match_views import Matches, MatchDetail

urlpatterns = [
    path('tournaments/', Tournaments.as_view(), name='tournaments'),
    path('tournaments/<int:pk>/', TournamentDetail.as_view(), name='tournament-detail'),
    path('tournaments/<int:t_pk>/players/', Players.as_view(), name='players'),
    path('tournaments/<int:t_pk>/matches/', Matches.as_view(), name='tournament-matches'),
    path('tournaments/<int:t_pk>/matches/<int:m_pk>/', MatchDetail.as_view(), name='tournament-match-detail'),
]
