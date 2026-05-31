
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import BlogPostForm, CategoryForm, EditUserForm, AddUserForm
from blogs.models import Blog, Category, Comment


from .models import (
    BlogAnalytics,
    SiteSettings
)
from datetime import date, timedelta
from django.utils import timezone



@login_required(login_url='login')
def dashboard(request):

    category_count = Category.objects.count()

    blogs_count = Blog.objects.count()

    users_count = User.objects.count()
    
    comments_count = Comment.objects.count()
    
    latest_user = User.objects.last()

    latest_comment = Comment.objects.last()

    latest_post = Blog.objects.last()

    published_posts = Blog.objects.filter(
        status='Published'
    ).count()

    draft_posts = Blog.objects.filter(
        status='Draft'
    ).count()

    featured_posts = Blog.objects.filter(
        is_featured=True
    ).count()

    ai_posts = Blog.objects.filter(
        is_ai_generated=True
    ).count()

    analytics = BlogAnalytics.objects.first()

    context = {

        'category_count': category_count,

        'blogs_count': blogs_count,

        'users_count': users_count,
        
        'comments_count': comments_count,

        'published_posts': published_posts,

        'draft_posts': draft_posts,

        'featured_posts': featured_posts,

        'ai_posts': ai_posts,

        'analytics': analytics,
        
        'latest_user': latest_user,
        
        'latest_comment': latest_comment,
       
        'latest_post': latest_post,
        
        

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )

@login_required(login_url='login')
def posts(request):

    search = request.GET.get('search')
    status = request.GET.get('status')

    posts = Blog.objects.all()

    if search:

        posts = posts.filter(
            title__icontains=search
        )

    if status and status != 'All':

        posts = posts.filter(
            status=status
        )

    posts = posts.order_by(
        '-created_at'
    )

    context = {
        'posts': posts
    }

    return render(
        request,
        'dashboard/posts.html',
        context
    )
@login_required(login_url='login')
def add_post(request):

    if request.method == 'POST':

        form = BlogPostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user

            post.save()

            form.save_m2m()

            return redirect(
                'posts'
            )

    else:

        form = BlogPostForm()

    context = {

        'form': form

    }

    return render(
        request,
        'dashboard/add_post.html',
        context
    )
    
@login_required(login_url='login')
def edit_post(request, id):

    post = get_object_or_404(
        Blog,
        id=id
    )

    if request.method == 'POST':

        form = BlogPostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect(
                'posts'
            )

    else:

        form = BlogPostForm(
            instance=post
        )

    context = {

        'form': form,
        'post': post

    }

    return render(
        request,
        'dashboard/edit_post.html',
        context
    )
@login_required(login_url='login')
def draft_posts(request):

    posts = Blog.objects.filter(
        status='Draft'
    ).order_by('-created_at')

    return render(
        request,
        'dashboard/posts.html',
        {
            'posts': posts
        }
    )


@login_required(login_url='login')
def featured_posts(request):

    posts = Blog.objects.filter(
        is_featured=True
    ).order_by('-created_at')

    return render(
        request,
        'dashboard/posts.html',
        {
            'posts': posts
        }
    )



@login_required(login_url='login')
def add_category(request):

    if request.method == 'POST':

        form = CategoryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'categories'
            )

    else:

        form = CategoryForm()

    return render(
        request,
        'dashboard/add_category.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def edit_category(request, id):

    category = get_object_or_404(
        Category,
        id=id
    )

    if request.method == 'POST':

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            form.save()

            return redirect(
                'categories'
            )

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        'dashboard/edit_category.html',
        {
            'form': form,
            'category': category
        }
    )


@login_required(login_url='login')
def delete_category(request, id):

    category = get_object_or_404(
        Category,
        id=id
    )

    category.delete()

    return redirect(
        'categories'
    )

@login_required(login_url='login')
def comments(request):

    comments = Comment.objects.select_related(
        'user',
        'blog'
    ).order_by('-created_at')

    context = {

        'comments': comments

    }

    return render(
        request,
        'dashboard/comments.html',
        context
    )
@login_required(login_url='login')
def delete_comment(request, id):

    comment = get_object_or_404(
        Comment,
        id=id
    )

    comment.delete()

    return redirect(
        'comments'
    )
    
@login_required(login_url='login')
def users(request):

    users = User.objects.all().order_by('-id')

    return render(
        request,
        'dashboard/users.html',
        {
            'users': users
        }
    )


@login_required(login_url='login')
def add_user(request):

    if request.method == 'POST':

        form = AddUserForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'users'
            )

    else:

        form = AddUserForm()

    return render(
        request,
        'dashboard/add_user.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def edit_user(request, id):

    user = get_object_or_404(
        User,
        id=id
    )

    if request.method == 'POST':

        form = EditUserForm(
            request.POST,
            instance=user
        )

        if form.is_valid():

            form.save()

            return redirect(
                'users'
            )

    else:

        form = EditUserForm(
            instance=user
        )

    return render(
        request,
        'dashboard/edit_user.html',
        {
            'form': form,
            'user': user
        }
    )


@login_required(login_url='login')
def delete_user(request, id):

    user = get_object_or_404(
        User,
        id=id
    )

    user.delete()

    return redirect(
        'users'
    )
    
@login_required(login_url='login')
def delete_post(request, id):

    post = get_object_or_404(
        Blog,
        id=id
    )

    post.delete()

    return redirect(
        'posts'
    )
@login_required(login_url='login')
def categories(request):

    search = request.GET.get('search')

    categories = Category.objects.all()

    if search:

        categories = categories.filter(
            category_name__icontains=search
        )

    categories = categories.order_by(
        '-created_at'
    )

    return render(
        request,
        'dashboard/categories.html',
        {
            'categories': categories
        }
    )
@login_required(login_url='login')
def ai_tools(request):

    return render(
        request,
        'dashboard/ai_tools.html'
    )


@login_required(login_url='login')
def ai_blog_generator(request):

    generated_blog = ""

    if request.method == "POST":

        topic = request.POST.get('topic')

        generated_blog = f"""
        This is AI generated blog content about {topic}.
        """

    return render(
        request,
        'dashboard/ai_blog_generator.html',
        {
            'generated_blog': generated_blog
        }
    )


@login_required(login_url='login')
def seo_generator(request):

    meta_title = ""
    meta_description = ""

    if request.method == "POST":

        keyword = request.POST.get(
            'keyword'
        )

        meta_title = f"{keyword} | Complete Guide 2026"

        meta_description = (
            f"Learn everything about {keyword}. "
            f"Complete guide, tips, benefits and best practices."
        )

    return render(
        request,
        'dashboard/seo_generator.html',
        {
            'meta_title': meta_title,
            'meta_description': meta_description
        }
    )


@login_required(login_url='login')
def content_rewriter(request):

    rewritten_content = ""

    if request.method == "POST":

        content = request.POST.get(
            'content'
        )

        rewritten_content = (
            f"Rewritten Version:\n\n{content}"
        )

    return render(
        request,
        'dashboard/content_rewriter.html',
        {
            'rewritten_content': rewritten_content
        }
    )


@login_required(login_url='login')
def ai_assistant(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get(
            'question'
        )

        answer = (
            f"AI Response for: {question}"
        )

    return render(
        request,
        'dashboard/ai_assistant.html',
        {
            'answer': answer
        }
    )


   
@login_required(login_url='login')
def daily_report(request):

    today = timezone.now().date()

    context = {

        'posts':
        Blog.objects.filter(
            created_at__date=today
        ).count(),

        'published_posts':
        Blog.objects.filter(
            created_at__date=today,
            status='Published'
        ).count(),

        'draft_posts':
        Blog.objects.filter(
            created_at__date=today,
            status='Draft'
        ).count(),

        'comments':
        Comment.objects.filter(
            created_at__date=today
        ).count(),

        'users':
        User.objects.filter(
            date_joined__date=today
        ).count(),

        'categories':
        Category.objects.filter(
            created_at__date=today
        ).count(),

        'report_date': today

    }

    return render(
        request,
        'dashboard/daily_report.html',
        context
    )
@login_required(login_url='login')
def weekly_report(request):

    week_ago = timezone.now() - timedelta(days=7)

    context = {

        'posts':
        Blog.objects.filter(
            created_at__gte=week_ago
        ).count(),

        'published_posts':
        Blog.objects.filter(
            created_at__gte=week_ago,
            status='Published'
        ).count(),

        'draft_posts':
        Blog.objects.filter(
            created_at__gte=week_ago,
            status='Draft'
        ).count(),

        'comments':
        Comment.objects.filter(
            created_at__gte=week_ago
        ).count(),

        'users':
        User.objects.filter(
            date_joined__gte=week_ago
        ).count(),

        'categories':
        Category.objects.filter(
            created_at__gte=week_ago
        ).count(),
        'report_date': timezone.now().date()

    }

    return render(
        request,
        'dashboard/weekly_report.html',
        context
    )
@login_required(login_url='login')
def monthly_report(request):

    now = timezone.now()

    context = {

        'posts':
        Blog.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month
        ).count(),

        'published_posts':
        Blog.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month,
            status='Published'
        ).count(),

        'draft_posts':
        Blog.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month,
            status='Draft'
        ).count(),

        'comments':
        Comment.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month
        ).count(),

        'users':
        User.objects.filter(
            date_joined__year=now.year,
            date_joined__month=now.month
        ).count(),

        'categories':
        Category.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month
        ).count(),
        'report_date': timezone.now().date()

    }

    return render(
        request,
        'dashboard/monthly_report.html',
        context
    )
@login_required(login_url='login')
def yearly_report(request):

    year = timezone.now().year

    context = {

        'posts':
        Blog.objects.filter(
            created_at__year=year
        ).count(),

        'published_posts':
        Blog.objects.filter(
            created_at__year=year,
            status='Published'
        ).count(),

        'draft_posts':
        Blog.objects.filter(
            created_at__year=year,
            status='Draft'
        ).count(),

        'comments':
        Comment.objects.filter(
            created_at__year=year
        ).count(),

        'users':
        User.objects.filter(
            date_joined__year=year
        ).count(),

        'categories':
        Category.objects.filter(
            created_at__year=year
        ).count(),
        'report_date': timezone.now().date()

    }

    return render(
        request,
        'dashboard/yearly_report.html',
        context
    )