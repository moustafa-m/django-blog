from django import forms
from blog_app.models import BlogModel
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'text', 'category', 'main_img']
        widgets = {
            'text': SummernoteWidget(),
        }
    
    title = SummernoteTextField()
        