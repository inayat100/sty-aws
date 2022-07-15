from django import forms
from .models import POST,user_contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class post_form(forms.ModelForm):
    class Meta:
        model = POST
        fields = ['img','title','post']
        widgets = {
            'img': forms.FileInput(attrs=({'class':'form-control '})),
            'title': forms.TextInput(attrs=({'class':'form-control'})),
            'post': forms.Textarea(attrs=({'class':'form-control'})),
        }

class singup_form(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}),
                                help_text=('make a strong password'))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}),
        help_text=('make a strong password')
    )
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs=({'class': 'form-control '})),
            'first_name': forms.TextInput(attrs=({'class': 'form-control'})),
            'last_name': forms.TextInput(attrs=({'class': 'form-control'})),
            'email': forms.EmailInput(attrs=({'class': 'form-control'})),


        }

class singin_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password',]
        widgets = {
            'username': forms.TextInput(attrs=({'class': 'form-control '})),
            'password': forms.PasswordInput(attrs=({'class': 'form-control'})),
        }

class contact_form(forms.ModelForm):
    class Meta:
        model = user_contact
        fields = ['your_name', 'your_email', 'your_Number','write']
        widgets = {
            'your_name': forms.TextInput(attrs=({'class': 'form-control '})),
            'your_email': forms.EmailInput(attrs=({'class': 'form-control'})),
            'your_Number': forms.TextInput(attrs=({'class': 'form-control'})),
            'write': forms.Textarea(attrs=({'class': 'form-controlr w-100'})),
        }




