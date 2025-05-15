from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'
            
            
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input'
            
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','picture']
        widgets ={
            'bio': forms.Textarea(attrs={'rows': 3}),
            
        }
        labels ={
            
            'picture': 'Profile Picture'
        }
    