
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class CreateUserForm (forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم', max_length=30, help_text='اسم المستخدم يجب ان لا يحتوي على مسافات')
    email= forms.EmailField(label='البريد الألكتروني')

    first_name=forms.CharField(label='الاسم')
    last_name=forms.CharField(label='اللقب')
    password1=forms.CharField(label='كلمة السر ', widget=forms.PasswordInput, min_length=6)
    password2=forms.CharField(label='تأكيد كلمة السر  ' , widget=forms.PasswordInput, min_length=6)


    class Meta:
        model=User
        fields =('username','email','first_name','last_name','password1','password2')


    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1'] !=cd['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة ')

        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('يوجد اسم مستخدم مسجل بهذا الإسم.')
        return cd['username']




class LoginForm(forms.ModelForm):
    username=forms.CharField(label='إسم المستخدم')
    password=forms.CharField(label= 'كلمة المرور'  ,widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('username','password')

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='الاسم')
    last_name = forms.CharField(label='اللقب')
    email = forms.EmailField(label='البريد الألكتروني')
    field = forms.CharField(label='مجال التخصص')


    class Meta:
        model= User
        fields=('first_name','last_name','email','field')

class ProfileUpdateform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('image',)



