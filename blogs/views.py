from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .models import Blog, Category, Comment
from django.db.models import Q

import requests


# ================= CATEGORY POSTS ================= #

def posts_by_category(request, category_id):

    posts = Blog.objects.filter(
        status='Published',
        category=category_id
    )

    category = get_object_or_404(
        Category,
        pk=category_id
    )

    context = {

        'posts': posts,
        'category': category,

    }

    return render(
        request,
        'post_by_category.html',
        context
    )


# ================= BLOG DETAIL ================= #

def blogs(request, slug):

    single_blog = get_object_or_404(

        Blog,

        slug=slug,

        status='Published'

    )

    # COMMENT

    if request.method == 'POST':

        comment = Comment()

        comment.user = request.user

        comment.blog = single_blog

        comment.comment = request.POST['comment']

        comment.save()

        return HttpResponseRedirect(
            request.path_info
        )

    comments = Comment.objects.filter(
        blog=single_blog
    )

    comment_count = comments.count()

    context = {

        'single_blog': single_blog,

        'comments': comments,

        'comment_count': comment_count,

    }

    return render(
        request,
        'blogs.html',
        context
    )


# ================= SEARCH ================= #

def search(request):

    keyword = request.GET.get('keyword')

    blogs = Blog.objects.filter(

        Q(title__icontains=keyword) |

        Q(short_description__icontains=keyword) |

        Q(blog_body__icontains=keyword),

        status='Published'

    )

    context = {

        'blogs': blogs,

        'keyword': keyword,

    }

    return render(
        request,
        'search.html',
        context
    )


# ================= CONTENT SAFETY ================= #

def check_content_safe(text):

    bad_words = [

        'badword1',
        'badword2',
        'abuse'

    ]

    if not text:

        return True

    for word in bad_words:

        if word in text.lower():

            return False

    return True


# ================= IMAGE SAFETY ================= #

def check_image_safe(image):

    if image and image.size > 2 * 1024 * 1024:

        return False

    return True


# ================= SAVE BLOG ================= #

@csrf_exempt
def save_blog(request):

    if request.method == "POST":

        title = request.POST.get('title')

        category_id = request.POST.get(
            'category'
        )

        short_description = request.POST.get(
            'short_description'
        )

        content = request.POST.get(
            'blog_body'
        )

        image = request.FILES.get(
            'featured_image'
        )

        # REQUIRED VALIDATION

        if not title or not content:

            return JsonResponse({

                'error':
                '⚠️ Title and content required'

            })

        # CONTENT SAFETY

        if not check_content_safe(content):

            return JsonResponse({

                'error':
                '⚠️ Inappropriate content detected'

            })

        # IMAGE SAFETY

        if image and not check_image_safe(image):

            return JsonResponse({

                'error':
                '⚠️ Image too large (Max 2MB)'

            })

        # CATEGORY

        try:

            category = Category.objects.get(
                id=category_id
            )

        except:

            category = Category.objects.first()

        # SAVE BLOG

        Blog.objects.create(

            title=title,

            category=category,

            author=request.user,

            featured_image=image,

            short_description=short_description,

            blog_body=content,

            status='Draft'

        )

        messages.success(

            request,

            "✅ Blog saved as Draft"

        )

        return JsonResponse({

            'status':'success',

            'message':
            '✅ Blog saved as Draft'

        })

    return JsonResponse({

        'error':'Invalid Request'

    })


# ================= AUTO SAVE ================= #

@csrf_exempt
def autosave_blog(request):

    return JsonResponse({

        'status':'disabled'

    })


# ================= GRAMMAR CHECK ================= #

@csrf_exempt
def grammar_check(request):

    text = request.POST.get('text')

    if not text:

        return JsonResponse({

            'matches': []

        })

    try:

        response = requests.post(

            "https://api.languagetool.org/v2/check",

            data={

                "text": text,

                "language": "en-US"

            }

        )

        return JsonResponse(
            response.json()
        )

    except:

        return JsonResponse({

            'matches': []

        })


# ================= TONE CHECK ================= #

@csrf_exempt
def tone_check(request):

    text = request.POST.get(
        'text',
        ''
    ).lower()

    tone = "Neutral 😐"

    if "good" in text or "great" in text:

        tone = "Positive 😊"

    elif "bad" in text or "worst" in text:

        tone = "Negative 😡"

    return JsonResponse({

        'tone': tone

    })