# =========================================================
# KD AI ASSISTANT - ULTRA PREMIUM views.py
# FULLY UPGRADED PROFESSIONAL VERSION
# =========================================================

from django.shortcuts import (

    render,

    get_object_or_404

)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import random

from .models import (
    ChatHistory,
    SavedDraft
)

# =========================================================
# BLOG IMPORTS
# =========================================================

from blogs.models import Blog, Category
from django.contrib.auth.models import User

# =========================================================
# AI IMPORTS
# =========================================================

from .ai_engine import generate_ai_blog
from .grammar import grammar_check
from .seo import seo_analysis
from .tone import humanize_content

# =========================================================
# IMAGE IMPORTS
# =========================================================

from .image_utils import (

    get_pexels_images,

    download_and_compress_image,

    generate_blog_images

)

# =========================================================
# SERVICES
# =========================================================

from .services import (

    get_youtube_videos,
    generate_blog_meta,
    generate_related_links

)


# =========================================================
# CHATBOT PAGE
# =========================================================

def chatbot_page(request):

    return render(

        request,

        "chatbot/chatbot.html"

    )


# =========================================================
# AI BLOG LIST PAGE
# =========================================================

def ai_blog_list(request):

    featured_blogs = (

        ChatHistory.objects.filter(

            status="published",

            is_featured=True

        )

        .order_by("-created_at")

    )

    blogs = (

        ChatHistory.objects.filter(

            status="published"

        )

        .order_by("-created_at")

    )

    context = {

        "featured_blogs":
        featured_blogs,

        "blogs":
        blogs

    }

    return render(

        request,

        "chatbot/ai_blog_list.html",

        context

    )


# =========================================================
# AI BLOG DETAIL PAGE
# =========================================================

def ai_blog_detail(

    request,

    slug

):

    blog = get_object_or_404(

        ChatHistory,

        slug=slug,

        status="published"

    )

    # =====================================================
    # INCREASE VIEWS
    # =====================================================

    blog.views += 1

    blog.save()

    # =====================================================
    # RELATED BLOGS
    # =====================================================

    related_blogs = (

        ChatHistory.objects.filter(

            category=blog.category,

            status="published"

        )

        .exclude(id=blog.id)

        .order_by("-created_at")[:6]

    )
    # =====================================================
    # TAGS LIST
    # =====================================================

    tags_list = []
    if blog.tags:
     tags_list = [
        tag.strip()
        for tag in blog.tags.split(',')
    ]

    context = {

    "blog": blog,

    "related_blogs":
    related_blogs,

    "tags_list":
    tags_list

   }
    
    return render(

        request,

        "chatbot/ai_blog_detail.html",

        context

    )
         

# =========================================================
# GENERATE BLOG
# =========================================================

@csrf_exempt
def generate_blog(request):

    if request.method != "POST":

        return JsonResponse({

            "success":False,

            "message":"Invalid request"

        })

    try:

        body = json.loads(request.body)

        prompt = body.get(

            "prompt",

            ""

        ).strip()

        if not prompt:

            return JsonResponse({

                "success":False,

                "message":"Prompt missing"

            })

        # =================================================
        # GENERATE AI BLOG
        # =================================================

        ai_blog = generate_ai_blog(prompt)

        title = ai_blog.get(

            "title",

            "AI Blog"

        )

        content = ai_blog.get(

            "content",

            ""

        )

        faq = ai_blog.get(

            "faq",

            ""

        )

        conclusion = ai_blog.get(

            "conclusion",

            ""

        )

        category = ai_blog.get(

            "category",

            "General"

        )

        tags = ai_blog.get(

            "tags",

            "AI,Technology"

        )

        # =================================================
        # CONTENT CLEANING
        # =================================================

        content = content.strip()

        faq = faq.strip()

        conclusion = conclusion.strip()

        # =================================================
        # SEO
        # =================================================

        seo_score = seo_analysis(content)

        # =================================================
        # GRAMMAR
        # =================================================

        grammar_score = grammar_check(content)

        # =================================================
        # HUMANIZE
        # =================================================

        humanized_content = (

            humanize_content(content)

        )
        # =================================================
        # PROFESSIONAL HTML FORMATTING
        # =================================================

        formatted_content = f"""

        <div class="kd-detail-content">

        {humanized_content}

        </div>

         """

        # =================================================
        # GENERATE PROFESSIONAL IMAGES
        # =================================================

        image_package = generate_blog_images(

            title=title,

            category=category

        )

        images = image_package.get(

            "inline_images",

            []

        )

        featured_image = image_package.get(

            "featured_image",

            ""

        )

        # =================================================
        # REMOVE DUPLICATE IMAGES
        # =================================================

        unique_images = []

        used_images = set()

        for image in images:

            if image not in used_images:

                unique_images.append(image)

                used_images.add(image)

        images = unique_images[:6]

        # =================================================
        # VIDEO QUERY
        # =================================================

        video_query = f"""

        {title}
        {category}
        tutorial guide

        """

        # =================================================
        # VIDEOS
        # =================================================

        youtube_links = (

            get_youtube_videos(

                video_query

            )

        )

        # =================================================
        # REMOVE DUPLICATE VIDEOS
        # =================================================

        unique_videos = []

        used_embeds = set()

        for video in youtube_links:

            embed = video.get(

                "embed",

                ""

            )

            if embed not in used_embeds:

                unique_videos.append(video)

                used_embeds.add(embed)

        youtube_links = unique_videos[:4]

        # =================================================
        # EXTERNAL LINKS
        # =================================================

        external_links = (

            generate_related_links(

                category

            )

        )

        # =================================================
        # META DATA
        # =================================================

        meta_data = generate_blog_meta(

            title,

            category,

            content

        )

        # =================================================
        # SAVE CHAT HISTORY
        # =================================================

        blog = ChatHistory.objects.create(

            title=title,

            prompt=prompt,

            content=formatted_content,

            faq=faq,

            conclusion=conclusion,

            category=category,

            tags=tags,

            featured_image=featured_image,

            seo_score=seo_score,

            grammar_score=grammar_score,

            tone="Professional Human Style",

            youtube_links=youtube_links,

            image_gallery=images,

            reading_time=
            meta_data.get(

                "reading_time",

                "5 min read"

            ),

            status="published"

        )

        # =================================================
        # SAVE TO MAIN WEBSITE BLOGS
        # =================================================

        try:

            # =============================================
            # CATEGORY OBJECT
            # =============================================

            category_obj, created = Category.objects.get_or_create(

                category_name=category

            )

            # =============================================
            # DEFAULT AUTHOR
            # =============================================

            default_author = User.objects.first()

            # =============================================
            # PREVENT DUPLICATES
            # =============================================

            existing_blog = Blog.objects.filter(

                title=title

            ).first()

            if not existing_blog:

                # =========================================
                # CREATE BLOG
                # =========================================

                main_blog = Blog.objects.create(

                    title=title,

                    category=category_obj,

                    author=default_author,

                    short_description=content[:300],

                    blog_body=formatted_content,

                    status="Published",
                    
                    is_ai_generated=True,

                )

                # =========================================
                # DOWNLOAD FEATURED IMAGE
                # =========================================

                if featured_image:

                    compressed_image = (

                        download_and_compress_image(

                            featured_image,

                            title

                        )

                    )

                    if compressed_image:

                        main_blog.featured_image.save(

                            compressed_image.name,

                            compressed_image,

                            save=True

                        )

        except Exception as e:

            print(

                "MAIN WEBSITE BLOG SAVE ERROR:",

                e

            )

        # =================================================
        # RESPONSE
        # =================================================

        return JsonResponse({

            "success":True,

            "title":title,

            "slug":blog.slug,

            "content":humanized_content,

            "faq":faq,

            "conclusion":conclusion,

            "category":category,

            "tags":tags,

            "seo_score":seo_score,

            "grammar_score":grammar_score,

            "featured_image":featured_image,

            "images":images,

            "youtube_links":youtube_links,

            "external_links":external_links,

            "meta_data":meta_data,

            "reading_time":
            meta_data.get(

                "reading_time",

                "5 min read"

            ),

            "keywords":
            meta_data.get(

                "keywords",

                []

            )

        })

    except Exception as e:

        print(

            "BLOG GENERATION ERROR:",

            e

        )

        return JsonResponse({

            "success":False,

            "message":str(e)

        })


# =========================================================
# SAVE DRAFT
# =========================================================

@csrf_exempt
def save_blog(request):

    if request.method != "POST":

        return JsonResponse({

            "success":False

        })

    try:

        body = json.loads(request.body)

        title = body.get(

            "title",

            "Untitled Draft"

        )

        content = body.get(

            "content",

            ""

        )

        prompt = body.get(

            "prompt",

            ""

        )

        category = body.get(

            "category",

            "General"

        )

        SavedDraft.objects.create(

            title=title,

            prompt=prompt,

            content=content,

            category=category

        )

        return JsonResponse({

            "success":True,

            "message":
            "Draft saved successfully"

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)

        })


# =========================================================
# REWRITE BLOG
# =========================================================

@csrf_exempt
def rewrite_blog(request):

    if request.method != "POST":

        return JsonResponse({

            "success":False

        })

    try:

        body = json.loads(request.body)

        content = body.get(

            "content",

            ""

        )

        rewritten = (

            humanize_content(content)

        )

        return JsonResponse({

            "success":True,

            "rewritten":rewritten

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)

        })


# =========================================================
# SEO CHECK
# =========================================================

@csrf_exempt
def seo_check(request):

    try:

        body = json.loads(request.body)

        content = body.get(

            "content",

            ""

        )

        score = seo_analysis(content)

        return JsonResponse({

            "success":True,

            "score":score

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)

        })


# =========================================================
# GRAMMAR CHECK
# =========================================================

@csrf_exempt
def grammar_api(request):

    try:

        body = json.loads(request.body)

        content = body.get(

            "content",

            ""

        )

        score = grammar_check(content)

        return JsonResponse({

            "success":True,

            "score":score

        })

    except Exception as e:

        return JsonResponse({

            "success":False,

            "message":str(e)

        })


# =========================================================
# TRENDING BLOGS
# =========================================================

def trending_blogs(request):

    blogs = [

        "Best AI Tools",

        "Future of Artificial Intelligence",

        "Technology News",

        "Digital Marketing Trends",

        "Remote Freelancing Trends",

        "Startup Growth",

        "Online Learning Ideas",

        "Nature and Mental Health",

        "AI Automation Systems"

    ]

    random.shuffle(blogs)

    return JsonResponse({

        "success":True,

        "blogs":blogs[:8]

    })


# =========================================================
# YOUTUBE TEST
# =========================================================

def youtube_test(request):

    videos = [

        {

            "title":"AI Technology",

            "embed":
            "https://www.youtube.com/embed/jNQXAC9IVRw",

            "thumbnail":
            "https://img.youtube.com/vi/jNQXAC9IVRw/maxresdefault.jpg"

        },

        {

            "title":"Business Growth",

            "embed":
            "https://www.youtube.com/embed/ysz5S6PUM-U",

            "thumbnail":
            "https://img.youtube.com/vi/ysz5S6PUM-U/maxresdefault.jpg"

        }

    ]

    return JsonResponse({

        "success":True,

        "videos":videos

    })
    
    
    