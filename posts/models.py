from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator


# Create your models here.


# 1. Jana User model (AbstractUser)
# class CustomUser(AbstractUser):
#     # Qosimsha magluwmat kerek bolsa usi jerge qosamiz
#     phone_regex = RegexValidator(
#         regex=r'^\+?\d{9,15}$'
#         message="Telefon nomer '+998991234567' formatinda boliwi kerek."
#     )
#     phone_number = models.CharField(
#         validators=[phone_regex],   # Tekseriwshini qosamiz
#         max_length=13,
#         blank=True,
#         null=True
#     )



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='category', verbose_name="Kategoriya")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
    
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Kateqoriya ati")
    
    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Teg ati')
    posts = models.ManyToManyField(Post, related_name='tags', verbose_name='Tagdin postlari')
    
    def __str__(self):
        return self.name
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
