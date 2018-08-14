from rest_framework import serializers

from accounts.serializers import User, UserSerializer
from .models import Idea, Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('impact', 'ease', 'confidence', 'average',)


class IdeaSerializer(serializers.ModelSerializer):
    score = ScoreSerializer(required=True)
    # TODO: Make this read-only?
    user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all())

    class Meta:
        model = Idea
        fields = ('user', 'description', 'score')

    def create(self, validated_data):
        score_data = validated_data.pop('score')
        idea = Idea.objects.create(**validated_data)
        Score.objects.create(idea=idea, **score_data)
        return idea

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
