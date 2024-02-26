from blog_app import views
from django.urls import path
from blog_app import views

urlpatterns = [
    path('<id>', views.renderBlog, name="blog_article")
]
