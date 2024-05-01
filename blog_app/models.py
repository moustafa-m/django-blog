from django.db import models
from django.contrib.auth.models import User
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
    date = models.DateTimeField()
    slug = models.CharField(max_length=30, null=True, blank=True)
    
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
    
    def __str__(self):
        return self.title + " by " + self.owner.username
    
    def save(self, *args, **kwargs):
        #FIXME special unicode characters do not work
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    