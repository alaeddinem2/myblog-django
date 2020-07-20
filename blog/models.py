from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation



# Create your models here.



class Category (models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
       # return '/detail/{}'.format(self.pk)
       return reverse('detail',args=[self.pk])



class Post(models.Model):
    title=models.CharField(max_length=100)
    #content=models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    #content = RichTextField(blank=True, null=True)
    post_date=models.DateTimeField(default=timezone.now)
    post_update=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(default='None', upload_to='blog_pics')
    likes=models.ManyToManyField(User,related_name='blog_post')
    category=models.CharField(max_length=100)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')



    def __str__(self):
        return self.title

    def get_absolute_url(self):
       # return '/detail/{}'.format(self.pk)
       return reverse('detail',args=[self.pk])

    class Meta:
        ordering=('-post_date',)

class Comment(models.Model):
    name=models.CharField(max_length=50, verbose_name='الاسم')
    email=models.EmailField(verbose_name='البريد الإلكتروني')
    #body=models.TextField(verbose_name='نص التعليق')
    body=RichTextField(blank=True, null=True)
    comment_date=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')

    def __str__(self):
        return str('علق {} على {}'.format(self.name, self.post))
    class Meta:
        ordering=('-comment_date',)
