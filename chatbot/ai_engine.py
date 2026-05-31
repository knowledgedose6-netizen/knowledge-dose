# =========================================================
# KD AI ASSISTANT - ULTRA PREMIUM ai_engine.py
# FULLY UPGRADED PROFESSIONAL VERSION
# =========================================================

from groq import Groq

from django.conf import settings
from django.utils.text import slugify

from blogs.models import Category

import json
import re
import requests
import random
import textwrap


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(

    api_key=settings.GROQ_API_KEY

)


# =========================================================
# CLEAN JSON RESPONSE
# =========================================================

def clean_json_response(text):

    if not text:

        return ""

    text = text.strip()

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    text = re.sub(
        r'[\x00-\x1F]+',
        '',
        text
    )

    start_index = text.find("{")

    end_index = text.rfind("}") + 1

    if start_index != -1 and end_index != -1:

        text = text[
            start_index:end_index
        ]

    return text.strip()


# =========================================================
# FORMAT BLOG CONTENT
# =========================================================

def format_blog_content(content):

    if not content:

        return ""

    formatted = content

    # =============================================
    # CLEAN EXTRA SPACES
    # =============================================

    formatted = re.sub(

        r'\n{3,}',

        '\n\n',

        formatted

    )

    # =============================================
    # MAIN TITLE
    # =============================================

    formatted = re.sub(

        r'^# (.*?)$',

        r'<h1>\1</h1>',

        formatted,

        flags=re.MULTILINE

    )

    # =============================================
    # H2
    # =============================================

    formatted = re.sub(

        r'^## (.*?)$',

        r'<h2>\1</h2>',

        formatted,

        flags=re.MULTILINE

    )

    # =============================================
    # H3
    # =============================================

    formatted = re.sub(

        r'^### (.*?)$',

        r'<h3>\1</h3>',

        formatted,

        flags=re.MULTILINE

    )

    # =============================================
    # BOLD
    # =============================================

    formatted = re.sub(

        r'\*\*(.*?)\*\*',

        r'<strong>\1</strong>',

        formatted

    )

    # =============================================
    # BLOCKQUOTE
    # =============================================

    formatted = re.sub(

        r'^> (.*?)$',

        r'<blockquote>\1</blockquote>',

        formatted,

        flags=re.MULTILINE

    )

    # =============================================
    # LIST ITEMS
    # =============================================

    formatted = re.sub(

        r'^\- (.*?)$',

        r'<li>\1</li>',

        formatted,

        flags=re.MULTILINE

    )

    # =============================================
    # WRAP UL
    # =============================================

    formatted = re.sub(

        r'(<li>.*?</li>)',

        r'<ul>\1</ul>',

        formatted,

        flags=re.DOTALL

    )

    # =============================================
    # PARAGRAPHS
    # =============================================

    paragraphs = formatted.split("\n\n")

    final_paragraphs = []

    for para in paragraphs:

        para = para.strip()

        if not para:

            continue

        if para.startswith("<h"):

            final_paragraphs.append(para)

        elif para.startswith("<ul>"):

            final_paragraphs.append(para)

        elif para.startswith("<blockquote>"):

            final_paragraphs.append(para)

        else:

            final_paragraphs.append(

                f"<p>{para}</p>"

            )

    return "\n".join(final_paragraphs)


# =========================================================
# DETECT CATEGORY
# =========================================================

def detect_category(prompt):

    prompt = prompt.lower()

    categories = Category.objects.all()

    for category in categories:

        name = (
            category.category_name
            .lower()
        )

        if name in prompt:

            return category.category_name

        for word in name.split():

            if word in prompt:

                return category.category_name

    return "General"


# =========================================================
# GNEWS
# =========================================================

def get_latest_news(query):

    try:

        url ="https://gnews.io/api/v4/search"

        params = {

            "q":query,

            "lang":"en",

            "country":"pk",

            "max":5,

            "apikey":
            settings.GNEWS_API_KEY

        }

        response =requests.get(

            url,

            params=params,

            timeout=15

        )

        data =response.json()

        articles =data.get(
            "articles",
            []
        )

        news = ""

        for article in articles:

            news += f"""

            TITLE:
            {article.get('title')}

            DESCRIPTION:
            {article.get('description')}

            URL:
            {article.get('url')}

            """

        return news

    except Exception:

        return ""


# =========================================================
# YOUTUBE LINKS
# =========================================================

def get_youtube_links(query):

    try:

        return [

            {
                "title":"AI Technology Explained",

                "embed":
                "https://www.youtube.com/embed/jNQXAC9IVRw",

                "thumbnail":
                "https://img.youtube.com/vi/jNQXAC9IVRw/maxresdefault.jpg"
            },

            {
                "title":"Future Technology Trends",

                "embed":
                "https://www.youtube.com/embed/ysz5S6PUM-U",

                "thumbnail":
                "https://img.youtube.com/vi/ysz5S6PUM-U/maxresdefault.jpg"
            }

        ]

    except Exception:

        return []


# =========================================================
# EXTERNAL LINKS
# =========================================================

def generate_external_links(category):

    links = {

        "Technology":[

            "https://techcrunch.com",
            "https://www.theverge.com",
            "https://wired.com"

        ],

        "AI":[

            "https://openai.com",
            "https://huggingface.co",
            "https://deepmind.google"

        ],

        "Business":[

            "https://forbes.com",
            "https://entrepreneur.com"

        ],

        "Education":[

            "https://coursera.org",
            "https://edx.org"

        ],

        "Health":[

            "https://healthline.com",
            "https://webmd.com"

        ]

    }

    return links.get(
        category,
        [
            "https://google.com"
        ]
    )


# =========================================================
# CATEGORY STYLES
# =========================================================

CATEGORY_STYLES = {

    "AI":
    """
    Include:
    - AI automation
    - productivity
    - future AI
    - ethical concerns
    - modern tools
    - business impact
    """,

    "Technology":
    """
    Include:
    - futuristic innovation
    - cybersecurity
    - smart systems
    - practical use cases
    - future technology
    """,

    "Business":
    """
    Include:
    - startup growth
    - leadership
    - branding
    - strategy
    - future opportunities
    """,

    "Education":
    """
    Include:
    - smart learning
    - student mindset
    - digital education
    - future learning
    """,

    "General":
    """
    Include:
    - emotional storytelling
    - practical examples
    - modern insights
    - engaging hooks
    """
}


# =========================================================
# AI BLOG GENERATOR
# =========================================================

def generate_ai_blog(prompt):

    detected_category =detect_category(prompt)

    latest_news =get_latest_news(prompt)

    youtube_links =get_youtube_links(prompt)

    external_links =generate_external_links(
        detected_category
    )

    category_style =CATEGORY_STYLES.get(
        detected_category,
        CATEGORY_STYLES["General"]
    )

    final_prompt = f"""

You are KD AI Ultra Premium Blogging Engine.

Create a fully professional article.

STRICT RULES:

1. Use proper HTML style formatting
2. Use:
   - # Main Title
   - ## Headings
   - ### Subheadings
3. Add emotional storytelling
4. Add professional formatting
5. Add FAQs
6. Add bullet points
7. Add modern examples
8. Add expert writing tone
9. Add future insights
10. Add practical tips
11. Add conclusion
12. Add premium article structure
13. Add readability optimization
14. Add transition words
15. Add highly engaging writing
16. Minimum 1800+ words
17. Add SEO optimized formatting
18. Avoid robotic writing
19. Avoid plain essay style
20. Make it look like Medium/Forbes article

USER REQUEST:
{prompt}

CATEGORY:
{detected_category}

CATEGORY STYLE:
{category_style}

TRENDING NEWS:
{latest_news}

RETURN ONLY VALID JSON.

NO MARKDOWN.

JSON FORMAT:

{{
"title":"",
"slug":"",
"category":"{detected_category}",
"meta_description":"",
"tags":"",
"tone":"Professional Human Style",
"featured_image_prompt":"",
"inline_image_prompts":[
"",
"",
"",
""
],
"youtube_links":[],
"external_links":[],
"content":"",
"faq":"",
"conclusion":"",
"seo_score":95,
"grammar_score":95
}}

"""

    try:

        response =client.chat.completions.create(

            model=
            "meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {

                    "role":"system",

                    "content":
                    """
                    You are the world's best
                    premium blogging AI.
                    """

                },

                {

                    "role":"user",

                    "content":
                    final_prompt

                }

            ],

            temperature=1,

            top_p=0.95,

            max_tokens=7000

        )

        ai_response = (
            response
            .choices[0]
            .message.content
        )

        cleaned =clean_json_response(
            ai_response
        )

        try:

            result =json.loads(cleaned)

            # =============================================
            # SLUG
            # =============================================

            if not result.get("slug"):

                result["slug"] = slugify(

                    result.get(
                        "title",
                        "generated-blog"
                    )

                )

            # =============================================
            # FORMAT CONTENT
            # =============================================

            result["content"] = format_blog_content(

                result.get(
                    "content",
                    ""
                )

            )

            result["faq"] = format_blog_content(

                result.get(
                    "faq",
                    ""
                )

            )

            result["conclusion"] = format_blog_content(

                result.get(
                    "conclusion",
                    ""
                )

            )

            # =============================================
            # YOUTUBE
            # =============================================

            result[
                "youtube_links"
            ] = youtube_links

            # =============================================
            # EXTERNAL LINKS
            # =============================================

            result[
                "external_links"
            ] = external_links

            # =============================================
            # TAGS SAFETY
            # =============================================

            if not result.get("tags"):

                result["tags"] = (

                    "AI,Technology,"
                    "KnowledgeDose"

                )

            # =============================================
            # FAQ SAFETY
            # =============================================

            if not result.get("faq"):

                result["faq"] = """

<h2>Frequently Asked Questions</h2>

<p>
This topic is becoming increasingly important in the modern digital world.
</p>

"""

            # =============================================
            # CONCLUSION SAFETY
            # =============================================

            if not result.get("conclusion"):

                result["conclusion"] = """

<h2>Final Thoughts</h2>

<p>
The future of this industry looks highly promising with continuous innovation and technological growth.
</p>

"""

            return result

        except Exception:

            return {

                "title":
                f"The Future of {detected_category}",

                "slug":
                slugify(
                    f"future-of-{detected_category}"
                ),

                "category":
                detected_category,

                "meta_description":
                f"Professional blog about {detected_category}",

                "tags":
                f"{detected_category},AI,KnowledgeDose",

                "tone":
                "Professional Human Style",

                "featured_image_prompt":
                f"{detected_category} futuristic workspace",

                "inline_image_prompts":[

                    f"{detected_category} futuristic image",

                    f"{detected_category} realistic industry image",

                    f"{detected_category} premium technology",

                    f"{detected_category} business growth"

                ],

                "youtube_links":
                youtube_links,

                "external_links":
                external_links,

                "content":
                format_blog_content(cleaned),

                "faq":
                "<h2>FAQs</h2><p>No FAQs available.</p>",

                "conclusion":
                "<h2>Conclusion</h2><p>Future trends are evolving rapidly.</p>",

                "seo_score":95,

                "grammar_score":95

            }

    except Exception as e:

        return {

            "title":
            "AI Generation Error",

            "slug":
            "ai-generation-error",

            "category":
            detected_category,

            "meta_description":
            "AI blog generation failed",

            "tags":
            "AI,Error",

            "tone":
            "Professional",

            "featured_image_prompt":
            "AI futuristic workspace",

            "inline_image_prompts":[],

            "youtube_links":[],

            "external_links":[],

            "content":
            f"<p>ERROR: {str(e)}</p>",

            "faq":"",

            "conclusion":"",

            "seo_score":0,

            "grammar_score":0

        }


# =========================================================
# REWRITE CONTENT
# =========================================================

def rewrite_content(content):

    try:

        prompt = f"""

Rewrite this content professionally.

Make it:
- more emotional
- more engaging
- more readable
- more premium
- more human

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

            max_tokens=3500

        )

        return (
            response
            .choices[0]
            .message.content
        )

    except Exception as e:

        return f"Rewrite Error: {str(e)}"


# =========================================================
# HUMANIZER
# =========================================================

def humanize_content(content):

    try:

        prompt = f"""

Rewrite this content
to sound fully human.

Make it:
- emotional
- storytelling style
- natural
- conversational
- premium

CONTENT:
{content}

Return only humanized content.

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

    except Exception as e:

        return f"Humanizer Error: {str(e)}"


# =========================================================
# SEO IMPROVER
# =========================================================

def improve_seo(content):

    try:

        prompt = f"""

Improve SEO professionally.

Add:
- keyword optimization
- readability
- FAQs
- transition words
- headings
- SEO formatting

CONTENT:
{content}

Return only optimized content.

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

            temperature=0.7,

            max_tokens=3500

        )

        return (
            response
            .choices[0]
            .message.content
        )

    except Exception as e:

        return f"SEO Error: {str(e)}"


# =========================================================
# GRAMMAR FIX
# =========================================================

def grammar_fix_content(content):

    return content