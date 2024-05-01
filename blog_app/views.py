from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator
from blog_app.models import BlogModel

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

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
    ctxt = {
        'blog' : blog
    }
    return render(request, 'blog.html', ctxt)
