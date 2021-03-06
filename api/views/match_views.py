from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.shortcuts import get_object_or_404

from ..serializers import MatchSerializier
from ..models.match import Match
from ..models.tournament import Tournament

class Matches(APIView):
    # authentication_classes = ()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = MatchSerializier

    def get(self, request, t_pk):
        """Get request for individual Match"""
        tournament = get_object_or_404(Tournament, pk=t_pk)
        data = MatchSerializier(tournament.match_set.all(), many=True).data
        print(f"Matches for tournament {tournament.name}:", data)
        return Response(data)

    def post(self, request, t_pk):
        """Create a new Match"""
        tournament = get_object_or_404(Tournament, pk=t_pk)
        match = MatchSerializier(data=request.data['match'])
        if match.is_valid():
            match.save()
            return Response(match.data, status=status.HTTP_201_CREATED)
        else:
            return Response(match.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchDetail(APIView):
    # authentication_classes = ()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = MatchSerializier

    def get(self, request, t_pk, m_pk):
        """Get request for individual Match"""
        match = get_object_or_404(Match, pk=m_pk)
        data = MatchSerializier(match).data
        print(f"Match {m_pk}:", data)
        return Response(data)

    def delete(self, request, t_pk, m_pk):
        """Delete individual Match"""
        tournament = get_object_or_404(Tournament, pk=t_pk)
        match = get_object_or_404(Match, pk=m_pk)
        if not request.user.id == tournament.owner:
            raise PermissionDenied('Unauthorized, you do not own the tournament this match belongs to.')
        match.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, t_pk, m_pk):
        tournament = get_object_or_404(Tournament, pk=t_pk)
        match = get_object_or_404(Match, pk=m_pk)
        if not request.user.id == tournament.owner:
            raise PermissionDenied('Unauthorized, you do not own the tournament this match belongs to.')
        if request.data['match'].get('tournament', False):
            del request.data['match']['tournament']
        ms = MatchSerializier(match, data=request.data['match'])
        if ms.is_valid():
            ms.save()
            return Response(ms.data, status=status.HTTP_202_ACCEPTED)
