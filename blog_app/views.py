from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from blog_app.models import BlogModel
from blog_app.forms import BlogForm
import bleach

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

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
    paginator = Paginator(all_blogs, 9)
    page = request.GET.get('page')
    all_blogs = paginator.get_page(page)

    ctxt = {
        "all_blogs" : all_blogs,
    }
    return render(request, 'discover.html', ctxt)

def renderBlog(request, slug):
    blog = BlogModel.objects.get(slug=slug)
    is_owner = (request.user == blog.owner or request.user.is_superuser)
    ctxt = {
        'blog' : blog,
        'is_owner': is_owner,
        'slug': slug
    }
    return render(request, 'blog.html', ctxt)

@login_required
def editBlog(request, slug):
    print('######')
    print(slug)
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
