
from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm,UserUpdateForm,ProfileUpdateform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from blog.models import Post, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import User



def register(request):
    cat_menu = Category.objects.all()
    if request.method=='POST':
        register_form=CreateUserForm(request.POST)
        if register_form.is_valid():
            new_user=register_form.save(commit=False)
            #username=register_form.cleaned_data['username']
            new_user.set_password(register_form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, f'تهانينا  {new_user} لقد تمت عملية التسجيل بنجاح ')
            return redirect('login')


    else:
        register_form=CreateUserForm()

    return render(request,'user/register.html',{'title':'إنشاء حساب ','register_form':register_form,'cat_menu':cat_menu, })

def login_user(request):
    cat_menu = Category.objects.all()
    if request.method=='POST':
        form=LoginForm()
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'تم تسجيل دخولك بنجاح')
            return redirect('profile')
        else:
            messages.warning(request,'يوجد خطأ في إسم المستخدم أو كلمة المرور')

    else:
        form = LoginForm()

    context={
        'title':'تسجيل الدخول',
        'form':form,
        'cat_menu': cat_menu,
    }
    return render(request,'user/login.html',context)

def logout_user(request):
    cat_menu = Category.objects.all()
    logout(request)
    messages.success(request, 'تم تسجيل خروجك بنجاح')
    context = {
        'title': 'تسجيل الخروج',
        'cat_menu': cat_menu,

    }
    return render(request, 'user/logout.html', context)

@login_required(login_url='login')

def profile(request):
    cat_menu = Category.objects.all()
    posts=Post.objects.filter(author=request.user)
    page_list = Post.objects.filter(author=request.user)
    paginator = Paginator(page_list, 5)
    page = request.GET.get('page')

    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_page)
    context = {
        'title': 'الملف الشخصي',
        'posts':posts,
        'page':page,
        'page_list':page_list,
        'cat_menu':cat_menu,

    }
    return render(request, 'user/profile.html', context)

@login_required(login_url='login')
def profile_update(request):
    cat_menu = Category.objects.all()
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateform(request.POST,request.FILES,
                                       instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, 'تم تعديل الملف الشخصي الخاص بك ')
            return redirect('profile')
    else:
        user_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateform(instance=request.user.profile)

    context={
        'title':'تعديل الملف الشخصي ',
        'user_form':user_form,
         'profile_form':profile_form,
        'cat_menu': cat_menu,
    }

    return render(request,'user/profile_update.html',context)

