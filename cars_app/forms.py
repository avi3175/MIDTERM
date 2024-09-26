from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Comment



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=None,  
        error_messages={
            'required': 'Please enter a password.',
            'invalid': 'Invalid password format.',
        }
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text=None,  
        error_messages={
            'required': 'Please confirm your password.',
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'comment']  
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Add a comment...', 'rows': 3}),
        }
