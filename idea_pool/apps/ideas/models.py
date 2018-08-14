import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

logger = logging.getLogger('idea_pool.ideas.models')


class Idea(models.Model):
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Fields
    description = models.TextField()


class Score(models.Model):
    # Relation
    idea = models.OneToOneField('Idea', on_delete=models.CASCADE, related_name='score')

    # Fields
    impact = models.IntegerField(default=0.0)
    ease = models.IntegerField(default=0.0)
    confidence = models.IntegerField(default=0.0)
    average = models.FloatField(null=True, blank=True)

    def calculate_average(self):
        scores = [self.impact, self.ease, self.confidence]
        return round(sum(scores) / len(scores), 2)


# Signals
@receiver(post_save, sender=Score)
def score_calculate_average_score(sender, instance, **kwargs):
    """Signal to re-calculate Score.average every time it's updated."""
    logger.info("Signal post_save score... ")
    logger.info(kwargs)
    post_save.disconnect(score_calculate_average_score, sender=sender)
    instance.average = instance.calculate_average()
    instance.save()
    post_save.connect(score_calculate_average_score, sender=sender)
