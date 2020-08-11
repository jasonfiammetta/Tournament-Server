from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.tournament import Tournament
from .models.match import Match
from .models.player import Player
from .models.user import User

class MatchSerializier(serializers.ModelSerializer):
    # tournament_name = serializers.ReadOnlyField(source='tournament.name')
    player_1_name = serializers.ReadOnlyField(source='player_1.name')
    player_2_name = serializers.ReadOnlyField(source='player_2.name')

    class Meta:
        model = Match
        fields = ('id', 'player_1_name', 'player_2_name', 'tournament', 'created_at', 'updated_at')

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'tournament')

class TournamentSerializer(serializers.ModelSerializer):
    # owner_email = serializers.ReadOnlyField(source='owner.email')
    # players = PlayerSerializer(read_only=True, many=True)
    # print('tournament serializer players', players)
    # player_names = serializers.ReadOnlyField(map(lambda p: p.name, players.data))

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'game', 'description', 'owner', 'owner_email', 'players') #, 'player_names')
        # fields = ('as_dict',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
