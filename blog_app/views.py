from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from blog_app.models import BlogModel, CommentsModel
from blog_app.forms import BlogForm, SearchForm, CommentForm

# Create your views here.
def index(request):
    index_text = 'Welcome to Django Blog'
    ctxt = {
        'index_text': index_text,
    }
    return render(request, 'index.html', ctxt)

@login_required
def create(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.owner = request.user
            form_instance.save()
            
            slug = form_instance.slug
            return renderBlog(request, slug)
    else:
        form = BlogForm()
    ctxt = {
        "form" : form
    }
    return render(request, 'create.html', ctxt)

def discover(request):
    all_blogs = BlogModel.objects.all()
    
    form = SearchForm(request.GET or None)
    title = request.GET.get('title_filter')
    category = request.GET.get('category_select')
    if title != '' and title is not None:
        all_blogs = all_blogs.filter(title__contains=title)
    
    if category != '' and category is not None:
        all_blogs = all_blogs.filter(category__exact=category)
    
    paginator = Paginator(all_blogs, 9)
    page = request.GET.get('page')
    all_blogs = paginator.get_page(page)

    ctxt = {
        'all_blogs' : all_blogs,
        'form': form,
        # 'title_filter': title,
        # 'category_select': category,
    }
    return render(request, 'discover.html', ctxt)

def renderBlog(request, slug):
    if request.method ==  "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.owner = request.user
            form_instance.blog = BlogModel.objects.get(slug=slug)
            form_instance.save()
            return redirect(renderBlog, slug=slug)
    else:
        form = CommentForm()
    
    blog = BlogModel.objects.get(slug=slug)
    comments = CommentsModel.objects.filter(blog=blog)
    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    
    is_admin = request.user.is_superuser
    is_owner = (request.user == blog.owner or is_admin)
    ctxt = {
        'blog' : blog,
        'is_owner': is_owner,
        'is_admin': is_admin,
        'slug': slug,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog.html', ctxt)

@login_required
def editBlog(request, slug):
    blog = BlogModel.objects.get(slug=slug)
    if not (request.user == blog.owner or request.user.is_superuser):
        messages.error(request, "Access Denied")
        return render(request, 'index.html', {})
    
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form_instance = form.save(commit=False)
        form_instance.last_edit = timezone.now()
        form_instance.save()
        return redirect(renderBlog, slug=blog.slug)
    ctxt = {
        'form': form
    }
    return render(request, 'create.html', ctxt)
