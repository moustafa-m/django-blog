from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify

# Create your models here.
## run these commands to apply models
# python manage.py makemigrations
# python manage.py migrate

def getFileName(instance, filename):
        return "user_{0}/{1}".format(instance.owner.username, filename)
    
class BlogModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=30, default="", unique=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=30, null=True, blank=True)
    last_edit = models.DateTimeField(null=True, blank=True)
    main_img = models.ImageField(upload_to=getFileName, default="default.png")
    
    #TODO: how to have image rendered in correct slot in blog?
    # how to upload multiple images? use different model?
    # images = models.ImageField(upload_to=getFileName, null=True)
    
    CATEGORY = {
        'HW' : 'Hardware',
        'SW' : 'Software',
        'B' : 'Benchmarks',
        'MISC' : 'Miscellaneous',
    }
    category = models.CharField(max_length=20, choices=CATEGORY)
    
    __original_title = None
    
    def __str__(self):
        return self.title + " by " + self.owner.username
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_title = self.title

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        #FIXME special unicode characters do not work
        if not self.slug:
            self.slug = slugify(self.title)
        
        # source: https://stackoverflow.com/questions/1355150/when-saving-how-can-you-check-if-a-field-has-changed
        if self.title != self.__original_title:
            self.slug = slugify(self.title)
            self.__original_title = self.title
        
        return super().save(force_insert, force_update, *args, **kwargs)
        
    