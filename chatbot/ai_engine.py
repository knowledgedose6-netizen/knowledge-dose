from groq import Groq

from django.conf import settings

from blogs.models import Category

import json
import re


client = Groq(

    api_key=settings.GROQ_API_KEY

)


# ================= CLEAN JSON ================= #

def clean_json_response(text):

    text = text.strip()

    text = text.replace(
        '```json',
        ''
    )

    text = text.replace(
        '```',
        ''
    )

    text = re.sub(
        r'[\x00-\x1F]+',
        '',
        text
    )

    return text.strip()


# ================= DYNAMIC CATEGORY DETECTION ================= #

def detect_category(prompt):

    prompt = prompt.lower()

    categories = Category.objects.all()

    for category in categories:

        category_name = category.category_name.lower()

        # exact match

        if category_name in prompt:

            return category.category_name

        # split word matching

        category_words = category_name.split()

        for word in category_words:

            if word in prompt:

                return category.category_name

    return 'General'


# ================= AI BLOG GENERATOR ================= #

def generate_ai_response(prompt):

    detected_category = detect_category(
        prompt
    )

    final_prompt = f"""

    You are KD AI Blogging Assistant.

    Generate a highly professional SEO optimized blog article.

    BLOG CATEGORY:
    {detected_category}

    IMPORTANT REQUIREMENTS:

    - Minimum 700 words
    - Human-like writing style
    - SEO optimized
    - Add headings
    - Add FAQs
    - Add conclusion
    - Return ONLY valid JSON
    - No markdown
    - No explanations

    RETURN JSON FORMAT:

    {{
        "title": "",
        "slug": "",
        "category": "{detected_category}",
        "meta_description": "",
        "tags": "",
        "tone": "",
        "featured_image_prompt": "",
        "content": "",
        "faq": "",
        "conclusion": "",
        "seo_score": 95,
        "grammar_score": 95
    }}

    USER REQUEST:
    {prompt}

    """

    try:

        response = client.chat.completions.create(

            model="meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {
                    "role": "user",
                    "content": final_prompt
                }

            ],

            temperature=0.7,

            max_tokens=1400

        )

        text = response.choices[0].message.content

        cleaned_text = clean_json_response(
            text
        )

        try:

            return json.loads(cleaned_text)

        except json.JSONDecodeError:

            return {

                'title': 'Generated Blog',

                'slug': 'generated-blog',

                'category': detected_category,

                'meta_description':
                'AI generated professional blog',

                'tags':
                f'{detected_category}, AI Blog',

                'tone':
                'Professional',

                'featured_image_prompt':
                f'{detected_category} professional blog image',

                'content':
                cleaned_text,

                'faq': '',

                'conclusion': '',

                'seo_score': 90,

                'grammar_score': 90

            }

    except Exception as e:

        return {

            'title': 'AI Generation Error',

            'slug': 'ai-generation-error',

            'category': detected_category,

            'meta_description':
            'AI generation failed',

            'tags':
            'AI, Error',

            'tone':
            'Professional',

            'featured_image_prompt':
            'Modern AI technology workspace',

            'content':
            f'Error: {str(e)}',

            'faq': '',

            'conclusion': '',

            'seo_score': 0,

            'grammar_score': 0

        }


# ================= REWRITE CONTENT ================= #

def rewrite_content(content):

    try:

        prompt = f"""

        Rewrite this blog professionally.

        Return only rewritten content.

        CONTENT:
        {content}

        """

        response = client.chat.completions.create(

            model="meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.8,

            max_tokens=1200

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Rewrite Error: {str(e)}"


# ================= SEO OPTIMIZER ================= #

def improve_seo(content):

    try:

        prompt = f"""

        Improve SEO of this content.

        Return only optimized content.

        CONTENT:
        {content}

        """

        response = client.chat.completions.create(

            model="meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.5,

            max_tokens=1200

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"SEO Error: {str(e)}"


# ================= HUMANIZER ================= #

def humanize_content(content):

    try:

        prompt = f"""

        Rewrite this AI content to sound human.

        Return only humanized content.

        CONTENT:
        {content}

        """

        response = client.chat.completions.create(

            model="meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.9,

            max_tokens=1200

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Humanizer Error: {str(e)}"


# ================= GRAMMAR FIXER ================= #

def grammar_fix_content(content):

    try:

        prompt = f"""

        Correct grammar professionally.

        Return only corrected content.

        CONTENT:
        {content}

        """

        response = client.chat.completions.create(

            model="meta-llama/llama-4-scout-17b-16e-instruct",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.3,

            max_tokens=1200

        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Grammar Error: {str(e)}"