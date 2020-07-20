
from django import forms

from .models import Comment, Post, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class NewComment (forms.ModelForm):
     name=forms.CharField(label='الاسم')
     email=forms.EmailField(label='البريد الإلكتروني ')
     body=forms.CharField(label='نص التعليق', widget=CKEditorUploadingWidget())
     class Meta:
        model=Comment
        fields=('name','email','body')

#cats=[('sport','sport'),('politic','politic')]
choice=Category.objects.all().values_list('name','name')
class PostCreateForm (forms.ModelForm):
    title=forms.CharField(label='عنوان التدوينة')
    image=forms.FileField(label='أضف صورة للمدونة ')
    category=forms.ChoiceField(choices=choice, label='المجال')

    content=forms.CharField(label=   'نص التدوينة ' , widget=CKEditorUploadingWidget())

    class Meta:
       model = Post
       fields = ['title','category','content','image']










