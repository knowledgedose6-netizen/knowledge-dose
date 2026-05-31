# =========================================================
# KD AI ASSISTANT - voice.py
# ULTRA PREMIUM VOICE ENGINE
# =========================================================

import pyttsx3
import threading


# =========================================================
# INIT ENGINE
# =========================================================

engine = pyttsx3.init()


# =========================================================
# ENGINE SETTINGS
# =========================================================

engine.setProperty(

    'rate',

    170

)

engine.setProperty(

    'volume',

    1.0

)

voices =engine.getProperty(
    'voices'
)

if voices:

    engine.setProperty(

        'voice',

        voices[0].id

    )


# =========================================================
# SPEAK FUNCTION
# =========================================================

def speak(text):

    try:

        if not text:

            return

        engine.say(text)

        engine.runAndWait()

    except Exception as e:

        print(
            "VOICE ERROR:",
            e
        )


# =========================================================
# THREADED SPEAK
# =========================================================

def threaded_speak(text):

    try:

        thread =threading.Thread(

            target=speak,

            args=(text,)

        )

        thread.start()

    except Exception as e:

        print(
            "THREAD VOICE ERROR:",
            e
        )


# =========================================================
# STOP SPEAKING
# =========================================================

def stop_speaking():

    try:

        engine.stop()

    except Exception as e:

        print(
            "STOP ERROR:",
            e
        )


# =========================================================
# WELCOME MESSAGE
# =========================================================

def welcome_message():

    text = """

    Welcome to KnowledgeDose Blogging Website.

    I am KD AI.

    Which blog would you like to write today?

    """

    threaded_speak(text)


# =========================================================
# BLOG CREATED VOICE
# =========================================================

def blog_created_voice():

    threaded_speak(

        "Your blog has been successfully created."

    )


# =========================================================
# DRAFT SAVED VOICE
# =========================================================

def draft_saved_voice():

    threaded_speak(

        "Your draft has been saved successfully."

    )


# =========================================================
# SEO COMPLETE VOICE
# =========================================================

def seo_complete_voice():

    threaded_speak(

        "SEO optimization completed successfully."

    )


# =========================================================
# GRAMMAR COMPLETE VOICE
# =========================================================

def grammar_complete_voice():

    threaded_speak(

        "Grammar correction completed successfully."

    )


# =========================================================
# HUMANIZE COMPLETE VOICE
# =========================================================

def humanize_complete_voice():

    threaded_speak(

        "Content humanized successfully."

    )


# =========================================================
# ERROR VOICE
# =========================================================

def error_voice():

    threaded_speak(

        "Something went wrong. Please try again."

    )


# =========================================================
# LISTEN BLOG
# =========================================================

def listen_blog(content):

    try:

        cleaned =content.replace(
            "<br>",
            ""
        )

        threaded_speak(cleaned)

    except Exception as e:

        print(
            "LISTEN BLOG ERROR:",
            e
        )


# =========================================================
# NOTIFICATION VOICE
# =========================================================

def notification_voice(message):

    threaded_speak(message)