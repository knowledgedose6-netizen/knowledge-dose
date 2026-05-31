# =========================================================
# KD AI ASSISTANT - tone.py
# ULTRA PREMIUM HUMANIZER + TONE ENGINE
# =========================================================

from groq import Groq
from django.conf import settings

import random
import re


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(

    api_key=settings.GROQ_API_KEY

)


# =========================================================
# HUMAN TONES
# =========================================================

AVAILABLE_TONES = [

    "Professional",

    "Conversational",

    "Emotional",

    "Luxury",

    "Motivational",

    "Storytelling",

    "Friendly",

    "Premium Human Style",

    "Expert Blogger",

    "Modern Digital Tone"

]


# =========================================================
# DETECT TONE
# =========================================================

def detect_tone(content):

    try:

        content =content.lower()

        if any(word in content for word in [

            "motivation",
            "success",
            "mindset",
            "dream"

        ]):

            return "Motivational"

        if any(word in content for word in [

            "luxury",
            "premium",
            "fashion"

        ]):

            return "Luxury"

        if any(word in content for word in [

            "story",
            "journey",
            "experience"

        ]):

            return "Storytelling"

        if any(word in content for word in [

            "technology",
            "business",
            "ai"

        ]):

            return "Professional"

        return "Conversational"

    except Exception:

        return "Professional"


# =========================================================
# HUMANIZE CONTENT
# =========================================================

def humanize_content(content):

    try:

        prompt = f"""

Rewrite this content
to sound deeply human.

IMPORTANT RULES:

- make it emotional
- make it conversational
- make it storytelling style
- avoid robotic AI tone
- use transition words
- use modern human writing
- add emotional hooks
- improve readability
- improve flow
- premium writing style
- professional structure
- avoid repetitive wording
- natural English
- engaging tone
- modern blog style

CONTENT:
{content}

Return ONLY rewritten content.

"""

        response =client.chat.completions.create(

            model=
            "meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {

                    "role":"system",

                    "content":
                    """
                    You are the world's best
                    human blog rewriting engine.
                    """

                },

                {

                    "role":"user",

                    "content":
                    prompt

                }

            ],

            temperature=1,

            top_p=0.95,

            max_tokens=4000

        )

        rewritten = (

            response
            .choices[0]
            .message.content

        )

        return rewritten

    except Exception as e:

        return content


# =========================================================
# REWRITE PROFESSIONAL
# =========================================================

def rewrite_professionally(content):

    try:

        prompt = f"""

Rewrite this content professionally.

Make it:

- premium
- emotional
- engaging
- readable
- modern
- expert level

Avoid robotic AI writing.

CONTENT:
{content}

Return only rewritten content.

"""

        response =client.chat.completions.create(

            model=
            "meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {

                    "role":"user",

                    "content":
                    prompt

                }

            ],

            temperature=0.9,

            max_tokens=4000

        )

        return (

            response
            .choices[0]
            .message.content

        )

    except Exception:

        return content


# =========================================================
# EMOTIONAL REWRITE
# =========================================================

def emotional_rewrite(content):

    try:

        prompt = f"""

Rewrite this content emotionally.

Make readers feel:

- inspired
- emotionally connected
- curious
- motivated

Use storytelling style.

CONTENT:
{content}

Return only rewritten content.

"""

        response =client.chat.completions.create(

            model=
            "meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {

                    "role":"user",

                    "content":
                    prompt

                }

            ],

            temperature=1,

            max_tokens=3500

        )

        return (

            response
            .choices[0]
            .message.content

        )

    except Exception:

        return content


# =========================================================
# BLOG STYLE FORMATTER
# =========================================================

def blog_style_format(content):

    try:

        formatted = content

        # =============================================
        # CLEAN SPACES
        # =============================================

        formatted = re.sub(

            r'\n{3,}',

            '\n\n',

            formatted

        )

        # =============================================
        # CONVERT HEADINGS
        # =============================================

        formatted = formatted.replace(

            "## ",

            "<h2>"

        )

        formatted = formatted.replace(

            "### ",

            "<h3>"

        )

        return formatted

    except Exception:

        return content


# =========================================================
# HUMAN SCORE
# =========================================================

def human_score(content):

    try:

        score = 80

        emotional_words = [

            "journey",
            "future",
            "dream",
            "success",
            "innovation",
            "growth",
            "experience",
            "powerful",
            "transform"

        ]

        for word in emotional_words:

            if word.lower() in content.lower():

                score += 2

        if score > 100:

            score = 100

        return score

    except Exception:

        return 95


# =========================================================
# READABILITY IMPROVER
# =========================================================

def improve_readability(content):

    try:

        prompt = f"""

Improve readability professionally.

Make it:

- easy to read
- engaging
- modern
- premium
- human-like

Use:
- short paragraphs
- transition words
- clean structure

CONTENT:
{content}

Return only improved content.

"""

        response =client.chat.completions.create(

            model=
            "meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {

                    "role":"user",

                    "content":
                    prompt

                }

            ],

            temperature=0.8,

            max_tokens=3500

        )

        return (

            response
            .choices[0]
            .message.content

        )

    except Exception:

        return content


# =========================================================
# ENGAGEMENT SCORE
# =========================================================

def engagement_score(content):

    try:

        score = 75

        hooks = [

            "imagine",
            "what if",
            "surprising",
            "future",
            "secret",
            "discover"

        ]

        for hook in hooks:

            if hook in content.lower():

                score += 4

        if score > 100:

            score = 100

        return score

    except Exception:

        return 90


# =========================================================
# COMPLETE TONE REPORT
# =========================================================

def generate_tone_report(content):

    return {

        "tone":
        detect_tone(content),

        "human_score":
        human_score(content),

        "engagement_score":
        engagement_score(content)

    }