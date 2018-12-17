from rest_framework import serializers

from accounts.serializers import User, UserSerializer
from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all(),
                                              required=False, write_only=True)
    content = serializers.CharField(max_length=255)
    impact = serializers.IntegerField(min_value=1, max_value=10)
    ease = serializers.IntegerField(min_value=1, max_value=10)
    confidence = serializers.IntegerField(min_value=1, max_value=10)
    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Idea
        fields = ('user', 'uid', 'content', 'impact', 'ease', 'confidence', 'average_score',
                  'created')
