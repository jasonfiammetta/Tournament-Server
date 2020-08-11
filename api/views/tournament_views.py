from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.tournament import Tournament
from ..serializers import TournamentSerializer
from ..serializers import PlayerSerializer
from ..serializers import UserSerializer

# Authenticated Tournament view
class Tournaments(generics.ListCreateAPIView):
    # authentication_classes = ()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TournamentSerializer

    queryset = Tournament.objects.all()

    def get(self, request):
        """Index request"""
        tournaments = Tournament.objects.all()
        # tournaments = Tournament.objects.filter(owner=request.user.id)
        data = TournamentSerializer(tournaments, many=True).data
        # print('tournaments', data)
        return Response(data)

    def post(self, request):
        """Create request"""
        # Add user to request object
        request.data['tournament']['owner'] = request.user.id
        # request.data['tournament']['players'] = []
        playerList = request.data['tournament']['players']
        request.data['tournament']['players'] = []
        # Serialize/create tournament
        tournament = TournamentSerializer(data=request.data['tournament'])

        if tournament.is_valid():
            tournament.save()
            print('tournament', tournament.data)
            print('tournament [id]', tournament.data['id'])
            print('players to be added', playerList)
            for p in playerList:
                print('player', p)
                ps = PlayerSerializer(data={
                  'name': p,
                  'tournament': tournament.data['id']})
                if ps.is_valid():
                  ps.save()
            return Response(tournament.data, status=status.HTTP_201_CREATED)
        else:
            print('Bad request:', request.data)
            return Response(tournament.errors, status=status.HTTP_400_BAD_REQUEST)

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = ()
    permission_classes=(IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        """Show request"""
        tournament = get_object_or_404(Tournament, pk=pk)
        data = TournamentSerializer(tournament).data
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        print('delete request', request.data)
        tournament = get_object_or_404(Tournament, pk=pk)

        if not request.user.id == tournament.owner.id:
            print('User does not own Tournament')
            raise PermissionDenied('Unauthorized, you do not own this tournament')
        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        print('patch request', request.data)

        # Remove owner from request object
        if request.data['tournament'].get('owner', False):
            del request.data['tournament']['owner']

        # Locate Tournament
        tournament = get_object_or_404(Tournament, pk=pk)

        # Check if user is  the same
        if not request.user.id == tournament.owner.id:
            print('User does not own Tournament')
            raise PermissionDenied('Unauthorized, you do not own this tournament')

        # Add owner to data object now that we know this user owns the resource
        request.data['tournament']['owner'] = request.user.id
        # Validate updates with serializer
        ts = TournamentSerializer(tournament, data=request.data['tournament'], partial=True)
        if ts.is_valid():
            ts.save()
            print(ts)
            return Response(ts.data, status=status.HTTP_202_ACCEPTED)
        return Response(ts.errors, status=status.HTTP_400_BAD_REQUEST)
