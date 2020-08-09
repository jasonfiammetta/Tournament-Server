from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.tournament import Tournament
from ..serializers import TournamentSerializer, UserSerializer

# Create your views here.
class Tournaments(generics.ListCreateAPIView):
    def post(self, request):
        """Create request"""
        # Add user to request object
        request.data['tournament']['owner'] = request.user.id
        # request.data['tournament']['players'] = []
        # Serialize/create tournament
        tournament = TournamentSerializer(data=request.data['tournament'])
        print('tournament serializer:', tournament)
        if tournament.is_valid():
            m = tournament.save()
            return Response(tournament.data, status=status.HTTP_201_CREATED)
        else:
            print('Bad request:', request.data)
            return Response(tournament.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicTournaments(generics.ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = TournamentSerializer

    def get(self, request):
        """Index request"""
        tournaments = Tournament.objects.all()
        # tournaments = Tournament.objects.filter(owner=request.user.id)
        data = TournamentSerializer(tournaments, many=True).data
        print('tournaments', data)
        return Response(data)

class PublicTournamentsDetail(generics.ListCreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = TournamentSerializer

    def get(self, request, pk):
        """Index request"""
        tournament = get_object_or_404(Tournament, pk=pk)
        # tournaments = Tournament.objects.filter(owner=request.user.id)
        data = TournamentSerializer(tournament).data
        print('tournaments', data)
        return Response(data)

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        tournament = get_object_or_404(Tournament, pk=pk)
        data = TournamentSerializer(tournament).data
        # Only want to show owned tournaments?
        # if not request.user.id == data['owner']:
        #     raise PermissionDenied('Unauthorized, you do not own this tournament')
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        tournament = get_object_or_404(Tournament, pk=pk)
        if not request.user.id == tournament.owner:
            raise PermissionDenied('Unauthorized, you do not own this tournament')
        tournament.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        if request.data['tournament'].get('owner', False):
            del request.data['tournament']['owner']

        # Locate Tournament
        tournament = get_object_or_404(Tournament, pk=pk)
        # Check if user is  the same
        if not request.user.id == tournament.owner:
            raise PermissionDenied('Unauthorized, you do not own this tournament')

        # Add owner to data object now that we know this user owns the resource
        request.data['tournament']['owner'] = request.user.id
        # Validate updates with serializer
        ms = TournamentSerializer(tournament, data=request.data['tournament'])
        if ms.is_valid():
            ms.save()
            print(ms)
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
