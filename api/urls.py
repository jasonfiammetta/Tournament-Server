from django.urls import path
from .views.tournament_views import Tournaments, TournamentDetail, PublicTournaments, PublicTournamentsDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
	# Restful routing
    path('tournaments/', Tournaments.as_view(), name='tournaments'),
    path('tournaments/<int:pk>/', TournamentDetail.as_view(), name='tournament-detail'),
    path('get-tournaments/', PublicTournaments.as_view(), name='public-tournaments'),
    path('get-tournaments/<int:pk>/', PublicTournamentsDetail.as_view(), name='public-tournaments-detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
