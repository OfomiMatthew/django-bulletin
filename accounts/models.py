from django.db import models
from django.contrib.auth.models import User
from base.models import Post
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    picture = models.ImageField(upload_to='uploads/%Y/%m/%d',null=True,blank=True)
    favorite_posts = models.ManyToManyField(Post)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)


