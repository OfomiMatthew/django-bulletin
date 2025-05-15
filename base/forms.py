from .models import Contact,Post,Comment
from django import forms
from django.forms import ModelForm, Textarea


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact 
        fields = ['name','email','message']
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','picture','category','tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
         
            'picture': forms.ClearableFileInput(attrs={'class': 'input'}),
            'category': forms.Select(attrs={'class': 'select is-fullwidth'}),
            'tags': forms.SelectMultiple(attrs={'class': 'select is-multiple is-fullwidth'}),
        }
        labels = {
            'title': 'Title',
            
            'content': 'Content',
           
            'picture': 'Picture',
            'category': 'Category',
            'tags': 'Tags',
        }
    
class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write a comment...'})
    
    class Meta:
        model = Comment
        fields = ['text']
        labels ={
            'text': 'Comment'
        }
        widgets = {
            'text': Textarea(attrs={'rows': 3}),
        }