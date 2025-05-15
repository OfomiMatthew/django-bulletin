from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timezone import now
from django.contrib.auth.models import User


STATUS_CHOICES = [
    ('draft','Draft'),
    ('published','Published')
]

class Category(models.Model):
    title = models.CharField(max_length=100,verbose_name='Title')
    slug = models.SlugField(unique=True,max_length=200)
    
    
    class Meta:
        verbose_name='Category'
        verbose_name_plural = 'Categories'
        
    def get_absolute_url(self):
        return reverse('categories',args=[self.slug])
        
    def __str__(self):
        return self.title
    
    
  
class Tag(models.Model):
    title = models.CharField(max_length=200,verbose_name='Tag')
    slug = models.SlugField(max_length=200,unique=True)
    
    
    class Meta:
        verbose_name='Tag'
        verbose_name_plural = 'Tags'
        
    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])
    def __str__(self):
        return self.title
    
    
     
class Post(models.Model):
    title = models.CharField(max_length=300,verbose_name='Title')
    slug = models.SlugField(unique=True)
    content = RichTextUploadingField(verbose_name='Content')
    author = models.CharField(verbose_name="Created by", default="Anonymous",max_length=200)

    status = models.CharField(choices =STATUS_CHOICES,default='draft',max_length=10,verbose_name='status')
    publication_date = models.DateTimeField(verbose_name='Created',default=now)
    category = models.ForeignKey(Category,on_delete= models.CASCADE,verbose_name='Category')
    picture = models.ImageField(upload_to='uploads/%Y/%m/%d',null=True,blank=True)
    tags = models.ManyToManyField(Tag)
    likes = models.PositiveIntegerField(default=0)
    
    
    class Meta:
        verbose_name='Post'
        verbose_name_plural = 'Posts'
        
    def get_absolute_url(self):
        return reverse("bulletins",args=[self.slug])
    
    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=100,verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')
    message_date = models.DateField()
    
    def __str__(self):
        return f"{self.name} - {self.message_date}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    text = models.CharField(max_length=1000,verbose_name='Comment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
 
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
    
    
    

    