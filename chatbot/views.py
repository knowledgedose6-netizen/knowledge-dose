from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import json

from .ai_engine import (

    generate_ai_response,

    grammar_fix_content,

    humanize_content,

    improve_seo,

    rewrite_content

)

from .models import (

    AIBlogDraft,

    AIChatMessage

)

from .services import process_ai_content

from .image_utils import generate_ai_image


# ================= CHATBOT PAGE ================= #

def chatbot_page(request):

    return render(

        request,

        'chatbot/chatbot.html'

    )


# ================= GENERATE BLOG ================= #

@csrf_exempt
def generate_blog(request):

    data = json.loads(request.body)

    prompt = data.get('prompt')

    ai_data = generate_ai_response(
        prompt
    )

    processed_data = process_ai_content(
        ai_data
    )

    # AI IMAGE GENERATION

    image_url = generate_ai_image(

        processed_data[
            'featured_image_prompt'
        ]

    )

    processed_data[
        'image_url'
    ] = image_url

    # SAVE CHAT HISTORY

    AIChatMessage.objects.create(

        user=request.user
        if request.user.is_authenticated
        else None,

        chat_title=prompt[:50],

        message=prompt,

        response=processed_data[
            'content'
        ]

    )

    return JsonResponse(
        processed_data
    )


# ================= SAVE DRAFT ================= #

@csrf_exempt
def save_draft(request):

    data = json.loads(request.body)

    image_url = data.get(
        'image_url',
        ''
    )

    # FULL ABSOLUTE URL

    if image_url:

        image_url = request.build_absolute_uri(
            image_url
        )

    AIBlogDraft.objects.create(

        user=request.user
        if request.user.is_authenticated
        else None,

        title=data.get('title'),

        slug=data.get('slug'),

        category=data.get('category'),

        meta_description=
        data.get('meta_description'),

        tags=data.get('tags'),

        content=data.get('content'),

        # ✅ FIXED IMAGE URL
        featured_image_url=image_url,

        faq=data.get('faq'),

        conclusion=
        data.get('conclusion'),

        seo_score=
        data.get('seo_score'),

        grammar_score=
        data.get('grammar_score'),

        tone=data.get('tone'),

        ai_prompt=
        'AI Generated Prompt',

        publish_requested=True

    )

    return JsonResponse({

        'message':
        'Draft Saved & Sent To Admin'

    })


# ================= REWRITE ================= #

@csrf_exempt
def rewrite_blog(request):

    data = json.loads(request.body)

    content = data.get('content')

    response = rewrite_content(
        content
    )

    return JsonResponse({

        'response': response

    })


# ================= SEO ================= #

@csrf_exempt
def seo_blog(request):

    data = json.loads(request.body)

    content = data.get('content')

    response = improve_seo(
        content
    )

    return JsonResponse({

        'response': response

    })


# ================= HUMANIZE ================= #

@csrf_exempt
def humanize_blog(request):

    data = json.loads(request.body)

    content = data.get('content')

    response = humanize_content(
        content
    )

    return JsonResponse({

        'response': response

    })


# ================= GRAMMAR ================= #

@csrf_exempt
def grammar_blog(request):

    data = json.loads(request.body)

    content = data.get('content')

    response = grammar_fix_content(
        content
    )

    return JsonResponse({

        'response': response

    })


# ================= CHAT HISTORY ================= #

def get_chat_history(request):

    chats = AIChatMessage.objects.filter(

        user=request.user

    ).order_by('-created_at')

    data = []

    for chat in chats:

        data.append({

            'title':
            chat.chat_title,

            'message':
            chat.message,

            'response':
            chat.response

        })

    return JsonResponse({

        'chats': data

    })