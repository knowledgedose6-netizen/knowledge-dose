# =========================================================
# KD AI ASSISTANT - typing.py
# ULTRA PREMIUM TYPING ENGINE
# =========================================================

import time
import random
import threading


# =========================================================
# TYPING SPEEDS
# =========================================================

SLOW_SPEED = 0.08

NORMAL_SPEED = 0.04

FAST_SPEED = 0.02


# =========================================================
# SIMPLE TYPING EFFECT
# =========================================================

def typing_effect(

    text,

    speed=NORMAL_SPEED

):

    try:

        for char in text:

            print(

                char,

                end='',

                flush=True

            )

            time.sleep(speed)

        print()

    except Exception as e:

        print(
            "TYPING ERROR:",
            e
        )


# =========================================================
# PREMIUM TYPING
# =========================================================

def premium_typing(

    text,

    speed=FAST_SPEED

):

    try:

        for char in text:

            print(

                char,

                end='',

                flush=True

            )

            time.sleep(

                random.uniform(
                    speed,
                    speed + 0.03
                )

            )

        print()

    except Exception as e:

        print(
            "PREMIUM TYPING ERROR:",
            e
        )


# =========================================================
# AI THINKING EFFECT
# =========================================================

def ai_thinking():

    try:

        thinking = [

            "KD AI is thinking.",

            "KD AI is generating ideas..",

            "KD AI is creating premium content...",

            "KD AI is optimizing SEO...."

        ]

        for text in thinking:

            print(text)

            time.sleep(1)

    except Exception as e:

        print(
            "THINKING ERROR:",
            e
        )


# =========================================================
# TYPING ANIMATION
# =========================================================

def typing_animation(

    duration=3

):

    try:

        chars = [

            ".",

            "..",

            "...",

            "...."

        ]

        start =time.time()

        while (

            time.time() - start

        ) < duration:

            for char in chars:

                print(

                    f"\rKD AI Typing{char}",

                    end="",

                    flush=True

                )

                time.sleep(0.4)

        print()

    except Exception as e:

        print(
            "ANIMATION ERROR:",
            e
        )


# =========================================================
# STREAM RESPONSE
# =========================================================

def stream_response(

    text,

    speed=0.01

):

    try:

        words =text.split()

        for word in words:

            print(

                word,

                end=' ',

                flush=True

            )

            time.sleep(speed)

        print()

    except Exception as e:

        print(
            "STREAM ERROR:",
            e
        )


# =========================================================
# BACKGROUND TYPING
# =========================================================

def threaded_typing(

    text,

    speed=NORMAL_SPEED

):

    try:

        thread =threading.Thread(

            target=typing_effect,

            args=(text,speed)

        )

        thread.start()

    except Exception as e:

        print(
            "THREAD TYPING ERROR:",
            e
        )


# =========================================================
# LOADING BAR
# =========================================================

def loading_bar(

    total=20,

    speed=0.1

):

    try:

        print("Loading KD AI:")

        for i in range(total):

            print(

                "█",

                end='',

                flush=True

            )

            time.sleep(speed)

        print()

    except Exception as e:

        print(
            "LOADING BAR ERROR:",
            e
        )


# =========================================================
# BLOG GENERATION EFFECT
# =========================================================

def blog_generation_effect():

    try:

        messages = [

            "Generating Premium Headings...",

            "Creating SEO Structure...",

            "Adding Humanized Tone...",

            "Fetching Images...",

            "Embedding Videos...",

            "Optimizing Readability...",

            "Finalizing Blog..."

        ]

        for msg in messages:

            print(msg)

            time.sleep(1)

    except Exception as e:

        print(
            "BLOG EFFECT ERROR:",
            e
        )


# =========================================================
# SUCCESS MESSAGE
# =========================================================

def success_message():

    premium_typing(

        """

        Your premium blog has been
        successfully generated by KD AI.

        """,

        FAST_SPEED

    )


# =========================================================
# ERROR MESSAGE
# =========================================================

def error_message():

    premium_typing(

        """

        Something went wrong while
        generating your blog.

        Please try again.

        """,

        FAST_SPEED

    )


# =========================================================
# WELCOME EFFECT
# =========================================================

def welcome_typing():

    premium_typing(

        """

        Welcome to KnowledgeDose Blogging Website.

        I am KD AI.

        Which blog would you like to write today?

        """,

        NORMAL_SPEED

    )