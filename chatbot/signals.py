# =========================================================
# KD AI ASSISTANT - signals.py
# ULTRA PREMIUM SIGNALS
# =========================================================

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    ChatHistory,
    BlogAnalytics
)


# =========================================================
# CREATE ANALYTICS AUTOMATICALLY
# =========================================================

@receiver(post_save, sender=ChatHistory)
def create_blog_analytics(

    sender,

    instance,

    created,

    **kwargs

):

    try:

        if created:

            BlogAnalytics.objects.create(

                blog=instance,

                views=0,

                likes=0,

                shares=0,

                engagement_score=95,

                reading_time="5 min read"

            )

    except Exception as e:

        print(
            "SIGNAL ERROR:",
            e
        )


# =========================================================
# UPDATE ANALYTICS
# =========================================================

@receiver(post_save, sender=ChatHistory)
def update_blog_analytics(

    sender,

    instance,

    **kwargs

):

    try:

        analytics =BlogAnalytics.objects.filter(

            blog=instance

        ).first()

        if analytics:

            word_count =len(
                instance.content.split()
            )

            reading_minutes =max(
                1,
                round(word_count / 200)
            )

            analytics.reading_time = (
                f"{reading_minutes} min read"
            )

            analytics.save()

    except Exception as e:

        print(
            "ANALYTICS UPDATE ERROR:",
            e
        )