from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from ..models.tournament import Tournament
from ..models.player import Player
from ..serializers import TournamentSerializer, PlayerSerializer

class Players(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = PlayerSerializer

    def get(self, request, t_pk):
        tournament = get_object_or_404(Tournament, pk=t_pk)
        print('tournament players', tournament.players)
        data = PlayerSerializer(tournament.players, many=True).data
        return Response(data)

    def post(self, request, t_pk):
        tournament = get_object_or_404(Tournament, pk=t_pk)
        player_list = request.data['player_list']
        print('player list', player_list)
        if not request.user.id == tournament.owner.id:
            print('User does not own Tournament')
            raise PermissionDenied('Unauthorized, you do not own this tournament')
        print('tournament type', type(tournament))

        for p in player_list:
            print('player', p)
            ps = PlayerSerializer(data={
              'name': p,
              'tournament': tournament.id
            })
            if ps.is_valid():
              ps.save()
        data = TournamentSerializer(tournament).data
        data['player_names'] = []
        for p in data['players']:
            ps = get_object_or_404(Player, pk=p)
            data['player_names'].append(ps.name)
        return Response(data, status=status.HTTP_201_CREATED)
