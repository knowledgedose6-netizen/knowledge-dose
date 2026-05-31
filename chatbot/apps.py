# =========================================================
# KD AI ASSISTANT - apps.py
# =========================================================

from django.apps import AppConfig


class ChatbotConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'chatbot'

    verbose_name = "KD AI Assistant"

    def ready(self):

        try:

            import chatbot.signals

        except Exception:

            pass