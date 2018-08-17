from rest_framework import serializers

from accounts.serializers import User, UserSerializer
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all(),
                                              required=False, write_only=True)

    class Meta:
        model = Idea
        fields = ('user', 'uid', 'content', 'impact', 'ease', 'confidence', 'average_score',
                  'created')
