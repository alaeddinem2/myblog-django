from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from .models import Post, Comment,Category
from django.contrib import messages
from .forms import NewComment,PostCreateForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from . import models,forms
import requests

# Create your views here.

def category_view(request,cats):
    category_posts=Post.objects.filter(category=cats)
    cat_menu = Category.objects.all()
    context={
        'title':category_posts,
        'cats':cats.title(),

        'category_posts':category_posts,
        'cat_menu':cat_menu,
    }
    return render(request,'blog/categories.html',context)


def home(request):
    posts=Post.objects.all()
    paginator=Paginator(posts,5)
    page=request.GET.get('page')
    cat_menu=Category.objects.all()





    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
      posts = paginator.page(1)
    except EmptyPage:
      posts=paginator.page(paginator.num_page)

    context={
        "title":'الصفحة الرئيسية',
        "posts": posts,
        "page":page,

        "cat_menu":cat_menu,
    }
    return render(request,'blog/index.html',context)

def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d8eb4c2bcd92e0a3ac21eb6de3bfe536'
    data_weather=dict()
    city = request.GET.get('city')
    r = requests.get(url.format(city)).json()
    cat_menu = Category.objects.all()
    print(r)
    if r['cod'] == 200:
        data_weather = {
            'city': city,
            'temperateur': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        content = {'data_weather': data_weather,'cat_menu':cat_menu }

    else:
        #messages.warning(request, ' المدينة غير موجودة ')

         #return HttpResponseRedirect('weather/')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'blog/weather.html', content)

def about(request):
    cat_menu = Category.objects.all()
    context = {
        "title": 'من نحن',
        'cat_menu':cat_menu,

    }

    return render(request,'blog/about.html',context)

def project(request):
    cat_menu = Category.objects.all()
    context = {
        "title": 'المشروع',
        'cat_menu':cat_menu,

    }

    return render(request,'blog/project.html',context)




def post_detail(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    cat_menu = Category.objects.all()
    #total_likes=get_object_or_404(Post,pk=post_id)
    comments=post.comments.filter(active=True)
    #comments=post.comment

    if request.method=='POST':
        comment_form=NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            comment_form=NewComment()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    else:
        comment_form=NewComment

    context={
        'title':post,
        'post':post,
        'comments':comments,
        'comment_form':comment_form,
        'cat_menu':cat_menu,


    }
    return render(request, 'blog/detail.html', context)

def LikeView (request,pk):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def get_view_data(request,self, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        context = super(Post, self).get_context_data(**kwargs)
        context.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    #fields=['title','content']
    template_name = 'blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all()
        context=super(PostCreateView,self).get_context_data()
        context['cat_menu']=cat_menu
        return context

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all()
        context=super(PostUpdateView,self).get_context_data()
        context['cat_menu']=cat_menu
        return context


class PostDeleteView (UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all()
        context=super(PostDeleteView,self).get_context_data()
        context['cat_menu']=cat_menu
        return context

def delete_comment (request,post_id):
    Comment.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))















