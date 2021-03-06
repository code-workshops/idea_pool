import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shortuuidfield import ShortUUIDField
from model_utils.models import TimeStampedModel

from accounts.models import User

logger = logging.getLogger('idea_pool.ideas.models')


class Idea(TimeStampedModel):
    uid = ShortUUIDField()

    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')

    # Fields
    content = models.CharField(max_length=255)
    impact = models.IntegerField()
    ease = models.IntegerField()
    confidence = models.IntegerField()
    average_score = models.FloatField(null=True, blank=True)

    def calculate_average(self):
        scores = [self.impact, self.ease, self.confidence]
        return float(round(sum(scores) / len(scores), 1))


# Signals
@receiver(post_save, sender=Idea)
def calculate_average_score(sender, instance, **kwargs):
    """Signal to re-calculate Idea.average_score every time it's updated."""
    logger.info("Signal post_save score... ")
    logger.debug(kwargs)
    post_save.disconnect(calculate_average_score, sender=sender)
    instance.average_score = instance.calculate_average()
    instance.save()
    post_save.connect(calculate_average_score, sender=sender)
