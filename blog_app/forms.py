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

class SearchForm(forms.Form):
    title_filter = forms.CharField(label='Search Term:', required=False)
    
    # TODO: choices list is not dynamic
    category_select = forms.ChoiceField(label='Category:', required=False, choices=(('', ''),
                                                                                    ('HW', 'Hardware'),
                                                                                    ('SW', 'Software'),
                                                                                    ('B', 'Benchmarks'),
                                                                                    ('MISC', 'Miscellaneous')))